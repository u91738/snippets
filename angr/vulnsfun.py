#!/usr/bin/python3
import sys
import angr
import angrutils
import claripy

# Get func argument that leads to user-controlled instruction pointer or format string

binfile = 'test' if len(sys.argv) == 1 else sys.argv[1]
func_proto = 'void f(char *s)'
func_name = 'f'
# TODO: can we automatically get args from function prototype?
arg = claripy.BVS('s', 1024)

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
sim.explore()
angrutils.show_stash_sizes(sim)

# Look for user-controlled error strings
for i in sim.errored:
    print('Error state:', i.error)
    if 'Symbolic (format) string' in str(i.error):
        print(get_input(i.state).hex())

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
