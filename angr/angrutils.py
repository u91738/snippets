import angr


class BufferOverflowError(angr.SimError):
    pass


class __strcpy_chk(angr.SimProcedure):
    def run(self, dst, src, destlen):
        strlen = angr.SIM_PROCEDURES["libc"]["strlen"]
        strncpy = angr.SIM_PROCEDURES["libc"]["strncpy"]
        state = self.state

        src_len = self.inline_call(strlen, src).ret_expr
        overflow_cond = src_len >= destlen
        if state.solver.is_true(overflow_cond):
            state.add_constraints(overflow_cond)
            raise BufferOverflowError(f"__strcpy_chk: src length >= destlen ({destlen})")
        if not state.solver.is_false(overflow_cond):
            state.add_constraints(overflow_cond)
            raise BufferOverflowError(f"__strcpy_chk: src length may be >= destlen ({destlen})")
        return self.inline_call(strncpy, dst, src, src_len + 1, src_len=src_len).ret_expr


class __memcpy_chk(angr.SimProcedure):
    def run(self, dst, src, n, destlen):
        if self.state.solver.is_true(n > destlen) or not self.state.solver.is_false(n > destlen):
            self.state.add_constraints(n > destlen)
            raise BufferOverflowError(f"__memcpy_chk: n > destlen ({destlen})")
        return self.inline_call(angr.SIM_PROCEDURES["libc"]["memcpy"], dst, src, n).ret_expr


def init_project(proj):
    proj.hook_symbol("__strcpy_chk", __strcpy_chk())
    proj.hook_symbol("__memcpy_chk", __memcpy_chk())


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
    ini = proj.factory.full_init_state(add_options={angr.options.STRICT_PAGE_ACCESS, angr.options.ENABLE_NX})
    #ini = proj.factory.full_init_state()
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
