#!/usr/bin/python3

def get_file(state, fname):
    f = state.fs.get(fname)
    if f is None:
        return None
    else:
        return f.concretize()

def show_stash_inputs(stash, hex_print=False):
    for i in stash:
        print('------------')
        show_state_inputs(i, hex_print)

def show_state_inputs(state, hex_print=False):
    for fd, data in state.posix.fd.items():
        print('fd:', fd)
        o = state.posix.dumps(fd)
        print(o.hex() if hex_print else o)


def show_stash_sizes(sim):
    print('stashes')
    for key, stash in sim.stashes.items():
        print(key + ':', len(stash))
    print('errored:', len(sim.errored))
    print('')

def get_init_state(proj):
    '''Run init state until it branches'''
    ini = proj.factory.full_init_state()
    sim = proj.factory.simulation_manager(ini)
    while len(sim.active) == 1:
        last_state = sim.active[0]
        sim.step()
    return last_state

def step_until_first_change(sim, f):
    '''advance the sim until f(state) for some active state
    becomes different from initial f(sim.active[0])'''
    init = f(sim.active[0])
    while sim.active:
        sim.step()
        for a in sim.active:
            r = f(a)
            if r != init:
                return r
    return None
