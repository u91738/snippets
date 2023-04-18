#!/usr/bin/python3
import angr
import angrutils

binfile = 'test'

def get_input(state):
    return state.posix.dumps(0)

proj = angr.Project(binfile, load_options={'auto_load_libs': False, 'load_debug_info': True})

start_state = proj.factory.entry_state()

cfg=proj.analyses.CFGFast()

alloc_calls = []
try:
    malloc = proj.kb.functions['malloc'].addr
    alloc_calls.append(malloc)
except KeyError:
    malloc = None
try:
    calloc = proj.kb.functions['calloc'].addr
    alloc_calls.append(calloc)
except KeyError:
    calloc = None
try:
    realloc = proj.kb.functions['realloc'].addr
    alloc_calls.append(realloc)
except KeyError:
    realloc = None

assert alloc_calls, 'no allocation calls found in the binary'


sim = proj.factory.simulation_manager(start_state)
sim.use_technique(angr.exploration_techniques.MemoryWatcher())
sim.use_technique(angr.exploration_techniques.DFS())

sim.explore(find=alloc_calls, num_find=1024)
calls = sim.found.copy()
sim.found.clear()
for call in calls:
    sim.active[:] = [call]

    ip = call.solver.eval(call.regs.ip)
    if ip == malloc:
        alloc_size = call.regs.edi # obviously platform-dependent
        callname = 'malloc'
    elif ip == calloc:
        alloc_size = call.regs.edi * call.regs.esi
        callname = 'calloc'
    elif ip == realloc:
        alloc_size = call.regs.esi
        callname = 'realloc'
    else:
        assert False, "can't tell which call is used"

    result_ptr = angrutils.step_until_first_change(sim, lambda s: s.solver.eval(s.regs.rax))
    print('allocation returned:', hex(result_ptr))

    for a in sim.active:
        a.mem[result_ptr + alloc_size].uint32_t[0] = 0xDEADBEEF

    sim.explore(find=lambda s: s.solver.satisfiable([s.mem[result_ptr + alloc_size].uint32_t[0] != 0xDEADBEEF]))
    for f in sim.found:
        print(callname, ':', get_input(f).hex())
