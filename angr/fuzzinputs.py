#!/usr/bin/python3
import sys
import angr
import angrutils

# Find inputs for fuzzer
# Expects a binary with input from file passed as command line arg

# If it throws "TypeError: <BV64 strlen_11_64> doesn't fit in an argument of size 4"
# just try again

# CPython is a little faster than pypy3 on these scripts,
# even if https://docs.angr.io/en/latest/advanced-topics/speed.html#general-speed-tips
# says "Use pypy ... 10x speedup out of the box"

binfile = 'test' if len(sys.argv) == 1 else sys.argv[1]
input_fname, input_size = 'inp.txt', 300
timeout_seconds = 60


proj = angr.Project(binfile, load_options={'auto_load_libs': False}) # if you want libs, choose a few with 'preload_libs':['libsomething.so.1']
start_state = proj.factory.entry_state(args=[binfile, input_fname], fs={input_fname : angr.SimFile(input_fname, size=input_size)})
# May want to tweak:
# start_state.libc.buf_symbolic_bytes
# start_state.libc.max_buffer_size
# start_state.libc.max_strtol_size
# start_state.libc.max_str_len
# start_state.libc.max_variable_size

sim = proj.factory.simulation_manager(start_state, save_unconstrained=True)
sim.use_technique(angr.exploration_techniques.Timeout(timeout_seconds))
sim.use_technique(angr.exploration_techniques.MemoryWatcher()) # 95% RAM limit, if you really need more memory, see Spiller
sim.use_technique(angr.exploration_techniques.UniqueSearch())
# if UniqueSearch runs out of memory, try DFS + LengthLimiter

# for smaller search space LoopSeer might better prioritize states, needs normalized CFG
sim.explore()

angrutils.show_stash_sizes(sim)

for suffix, stash in sim.stashes.items():
    if suffix == 'errored':
        stash = sim.errored # errored from sim.stashes is empty for some reason
    for i, s in enumerate(stash):
        fname = f'{input_fname}{i}.{suffix}'
        print(suffix + ', writing input to', fname)
        state = s.state if suffix == 'errored' else s
        inp = angrutils.get_file(state, input_fname)
        if inp:
            print(inp.hex())
            with open(fname, 'wb') as f:
                f.write(inp)
        else:
            print('Failed to recover input for a state')
