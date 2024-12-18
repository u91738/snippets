#!/usr/bin/python3
import angr
import angrutils

binfile = 'test'

def get_input(state):
    return state.posix.dumps(0)

proj = angr.Project(binfile, load_options={'auto_load_libs': False, 'load_debug_info': True})
cc = proj.factory.cc()

start_state = proj.factory.entry_state()

cfg=proj.analyses.CFGFast()

alloc_calls = []
try:
    malloc = proj.kb.functions['malloc'].addr
    alloc_calls.append(malloc)
    malloc_proto = angr.sim_type.parse_signature('void *malloc(size_t size)')
except KeyError:
    malloc, malloc_proto = None, None
try:
    calloc = proj.kb.functions['calloc'].addr
    alloc_calls.append(calloc)
    calloc_proto = angr.sim_type.parse_signature('void *calloc(size_t nmemb, size_t size)')
except KeyError:
    calloc, calloc_proto = None, None
try:
    realloc = proj.kb.functions['realloc'].addr
    alloc_calls.append(realloc)
    realloc_proto = angr.sim_type.parse_signature('void *realloc(void *ptr, size_t size)')
except KeyError:
    realloc, realloc_proto = None

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
        [alloc_size] = cc.get_args(call, malloc_proto)
        callname = 'malloc'
        retloc = cc.return_val(malloc_proto.returnty)
    elif ip == calloc:
        [nmemb, size] = cc.get_args(call, calloc_proto)
        alloc_size = nmemb * size
        callname = 'calloc'
        retloc = cc.return_val(calloc_proto.returnty)
    elif ip == realloc:
        [alloc_size] = cc.get_args(call, realloc_proto)
        callname = 'realloc'
        retloc = cc.return_val(realloc_proto.returnty)
    else:
        assert False, "can't tell which call is used"

    result_ptr = angrutils.step_until_first_change(sim, lambda s: s.solver.eval(retloc.get_value(s)))
    print('allocation returned:', hex(result_ptr))

    for a in sim.active:
        a.mem[result_ptr + alloc_size].uint32_t[0] = 0xDEADBEEF

    sim.explore(find=lambda s: s.solver.satisfiable([s.mem[result_ptr + alloc_size].uint32_t[0] != 0xDEADBEEF]))
    for f in sim.found:
        print(callname, ':', get_input(f).hex())
