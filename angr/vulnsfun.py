#!env python3
import sys
from dataclasses import dataclass, field
from functools import reduce
from typing import Iterable, Tuple, Callable
from copy import deepcopy
from enum import Enum
import angr
import angrutils
import angr.claripy as c


def in_ranges(addr:c.ast.bv.BV, ranges:Iterable[Tuple[int, int]]) -> c.BoolV:
    if not ranges:
        return c.ast.bool.false()
    r = reduce(lambda a, b: a | b, [lo < addr <= hi for lo, hi in ranges])
    return r if isinstance(r, c.ast.bool.Bool) else c.BoolV(r)


def with_constraints(state: angr.SimState, constr) -> angr.SimState:
    r = state.copy()
    r.add_constraints(constr)
    return r if r.satisfiable() else None


@dataclass
class FindingInput:
    affected_address:int
    value:bytes

@dataclass
class Finding:
    kind: str
    message: str
    ip: list[int]
    inputs:list[FindingInput]


class StateValidator:
    '''Attach to angr sim state and watch for memory issues. Findings go to sim.stashes["state_validator_findings"]
       Angr passes weak references, so original state goes through deepcopy(), which can break some things.
    '''
    def __init__(
        self,
        project: angr.Project,
        sim: angr.SimulationManager,
        get_input:Callable[angr.SimState, bytes],
        stack_size: int = 8 * 1024 * 1024
    ):
        self.get_input = get_input
        self.project = project
        self.sim = sim
        self.max_enumerated_values = 4

        # Build these once. CLE objects expose segment permission properties.
        self._exec_ranges = []
        self._read_ranges = []
        self._write_ranges = []

        for obj in self.project.loader.all_objects:
            for seg in getattr(obj, "segments", []):
                try:
                    start = int(seg.vaddr)
                    end = start + int(seg.memsize)
                    if start < end:
                        r = (start, end)
                        if seg.is_executable:
                            self._exec_ranges.append(r)
                        if seg.is_writable:
                            self._write_ranges.append(r)
                        if seg.is_readable:
                            self._read_ranges.append(r)
                except (AttributeError, TypeError, ValueError):
                    pass

        self.stack_bound_high = project.arch.initial_sp
        self.stack_bound_low = self.stack_bound_high - stack_size

        self.null_page_end = project.loader.page_size if project.loader.page_size > 16 else 0x1000
        self._attached = set()
        self.__to_stop = set()
        self.findings = []


    def attach(self, states):
        for state in states:
            sid = id(state)
            if sid not in self._attached:
                self._attached.add(sid)
                state.inspect.b("mem_read", when=angr.BP_BEFORE, action=self._on_mem_read)
                state.inspect.b("mem_write", when=angr.BP_BEFORE, action=self._on_mem_write)
                state.inspect.b("exit", when=angr.BP_BEFORE, action=self._on_exit)
                state.inspect.b("irsb", when=angr.BP_AFTER, action=self._check_sp)


    def _check_sp(self, state: angr.SimState):
        if st := with_constraints(state, (state.regs.sp < self.stack_bound_low) | (state.regs.sp >= self.stack_bound_high)):
            self.__to_stop.add(id(state))
            self.findings.append(Finding(
                kind="SP_OUTSIDE_STACK",
                message="SP outside the configured stack range.",
                ip = self.__enumerate_values(st, st.regs.ip),
                inputs = self.__enumerate_values_w_inputs(st, st.regs.sp)
            ))


    def _on_mem_read(self, state: angr.SimState):
        if state.inspect.attrs.mem_read_address is not None:
            self._check_memory_address(state, state.inspect.attrs.mem_read_address, "read")


    def _on_mem_write(self, state: angr.SimState):
        if state.inspect.attrs.mem_write_address is not None:
            self._check_memory_address(state, state.inspect.attrs.mem_write_address, "write")

    def _check_memory_address(self, state: angr.SimState, addr, access: str):
        assert access in ('read', 'write')
        ranges = self._read_ranges if access == "read" else self._write_ranges

        if st := with_constraints(state, c.Not(in_ranges(addr, ranges))):
            self.__to_stop.add(id(state))
            self.findings.append(Finding(
                    kind=f"{access.upper()}_OUTSIDE_ALLOWED_MEMORY",
                    message=f"symbolic {access} address is outside the readable/writable image ranges.",
                    ip = self.__enumerate_values(st, st.regs.ip),
                    inputs = self.__enumerate_values_w_inputs(st, addr),
                ))
            return

        if st := with_constraints(state, addr < self.null_page_end):
            self.__to_stop.add(id(state))
            self.findings.append(Finding(
                    kind=f"{access.upper()}_CAN_HIT_NULL_PAGE",
                    message=f"Memory {access} in the null-page",
                    ip = self.__enumerate_values(st, st.regs.ip),
                    inputs = self.__enumerate_values_w_inputs(st, addr)
                ))


    def _on_exit(self, state: angr.SimState) -> None:
        if state.inspect.attrs.exit_target is None:
            return

        # Can jump actually happen?
        if state.inspect.attrs.exit_guard is  None:
            st_default = state
        else:
            st_default = state.copy()
            st_default.add_constraints(state.inspect.attrs.exit_guard)

        # Can jump can happen to non-executable memory?
        if st := with_constraints(st_default, c.Not(in_ranges(state.inspect.attrs.exit_target, self._exec_ranges))):
            self.__to_stop.add(id(state))
            self.findings.append(Finding(
                    kind="CONTROL_FLOW_OUTSIDE_EXECUTABLE",
                    message="control-flow successor lands outside executable memory",
                    ip = self.__enumerate_values(st, st.regs.ip),
                    inputs = self.__enumerate_values_w_inputs(st, st.inspect.attrs.exit_target),
                ))

        # Can jump can happen to writeable memory?
        if st := with_constraints(st_default, in_ranges(state.inspect.attrs.exit_target, self._write_ranges)):
            self.__to_stop.add(id(state))
            self.findings.append(Finding(
                    kind='CONTROL_FLOW_TO_WRITABLE_MEMORY',
                    message="control-flow successor lands in writeable memory",
                    ip = self.__enumerate_values(st, st.regs.ip),
                    inputs = self.__enumerate_values_w_inputs(st, st.inspect.attrs.exit_target)
                ))


    def on_step(self, simgr:angr.SimulationManager):
        simgr.drop(lambda st: id(st) in self.__to_stop)


    def __enumerate_values(self, state: angr.SimState, expr) -> list[int]:
        try:
            values = set([state.solver.min(expr), state.solver.max(expr)])
            if self.max_enumerated_values > 2:
                for x in state.solver.eval_upto(expr, self.max_enumerated_values - 2):
                    values.add(int(x))
            return sorted(values)
        except Exception as e:
            print(e, file=sys.stderr)
            return []

    def __enumerate_values_w_inputs(self, state: angr.SimState, expr) -> list[FindingInput]:
        try:
            r = []
            for v in self.__enumerate_values(state, expr):
                r.append(FindingInput(v, self.get_input(state)))
            return r
        except Exception as e:
            print(e, file=sys.stderr)
            return []


# Get func argument that leads to user-controlled instruction pointer or format string
binfile = 'test' if len(sys.argv) == 1 else sys.argv[1]
func_proto = 'void f(char *s)'
func_name = 'f'
arg = c.Concat(c.BVS('s', 8 * 127), c.BVV(0, 8))

def get_input(state):
    return state.solver.eval(arg, cast_to=bytes)

# Load project
proj = angr.Project(binfile, load_options={'auto_load_libs': False, 'load_debug_info': True})

# Get function address
cfg = proj.analyses.CFGFast()
fun_addr = proj.kb.functions[func_name].addr

# Prepare call state
ini = angrutils.get_init_state(proj)
start_state = proj.factory.call_state(fun_addr, angr.calling_conventions.PointerWrapper(arg, buffer=True), prototype=func_proto, base_state=ini, remove_options=angr.options.ALL_FILES_EXIST)

# Search
sim = proj.factory.simulation_manager(start_state, save_unconstrained=True)
sim.use_technique(angr.exploration_techniques.MemoryWatcher())

validator = StateValidator(proj, sim, get_input)
validator.attach([start_state])
sim.explore(step_func=validator.on_step)
angrutils.show_stash_sizes(sim)

# Look for user-controlled error strings
for i in sim.errored:
    print('Error state:', i.error)
    if ('Symbolic (format) string' in str(i.error)):
        # Try to find an input that has symbolic format string and can fit "%s"
        st = i.state.copy()
        arg_bytes = arg.chop(8)
        constraints = []
        for i in range(len(arg_bytes) - 1):
            constraints.append(c.And(arg_bytes[i] == ord('%'), arg_bytes[i + 1] == ord('s')))
        st.add_constraints(c.Or(*constraints))
        inp = get_input(st)
        #if inp is None:
        #    inp = get_input(i.state)
        print(inp)

# Overwrites of return address or function pointers will lead to unconstrained states
for s in sim.unconstrained:
    try:
        ip_wanted = next(i for i in [0xDEADBEEF, 0x10ADBEEF, 0x01ADBEEF, 0xADBEEF, 0xBEEF] if s.solver.satisfiable([s.regs.ip == i]))
    except StopIteration:
        ip_min = s.solver.min(s.regs.ip)
        ip_max = s.solver.max(s.regs.ip)
        print('Failed to pick a nice address to jump between', hex(ip_min), hex(ip_max), 'best try to produce input:')
        print(get_input(s).hex())
    else:
        s.add_constraints(s.regs.ip == ip_wanted)
        inp = get_input(s)
        if inp:
            ip_size = int(ip_wanted.bit_count() / 8 + 1)
            leip = ip_wanted.to_bytes(ip_size, 'little').hex()
            beip = ip_wanted.to_bytes(ip_size, 'big').hex()
            print(f'input leading to execution at 0x{leip} / 0x{beip}')
            print(inp.hex())
        else:
            print('Failed to recover input for unconstrained state')


for s in validator.findings:
    print(s.kind)
    for i in s.inputs:
        print(i.value)
    print()
