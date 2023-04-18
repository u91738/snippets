#!/usr/bin/python3
import angr

binfile = 'test'

def get_input(state):
    return state.posix.dumps(0)

proj = angr.Project(binfile, load_options={'auto_load_libs': False, 'load_debug_info': True})

start_state = proj.factory.entry_state()

cfg=proj.analyses.CFGFast()
free = proj.kb.functions['free'].addr

sim = proj.factory.simulation_manager(start_state)
sim.use_technique(angr.exploration_techniques.MemoryWatcher())
sim.use_technique(angr.exploration_techniques.DFS())

sim.explore(find=free, num_find=1024)
calls = sim.found.copy()
sim.found.clear()
for call in calls:
    sim.active[:] = [call]
    arg = call.solver.eval(call.regs.rdi)

    sim.step()

    sim.explore(find=lambda s: s.solver.eval((s.regs.ip == free) & (s.regs.rdi == arg)))
    for f in sim.found:
        print('double free:', get_input(f).hex())
