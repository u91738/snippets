#!/usr/bin/python3
from dataclasses import dataclass
import gdb

# This script follows some crypto operations
# and checks that you did not leave key or plain text
# in memory after you are done
#
# catch key passed to EVP_EncryptInit_ex
# plaintext in EVP_EncryptUpdate
# then search memory for these values
# at a later point when it is done (here - call to hexdump)
#
# Run with
# gdb --command sensitive_data.py -nh -batch encrypt


###########################################################
# Memory mapping classes to search memory for values
###########################################################

@dataclass
class Mapping:
    start_addr: int
    end_addr: int
    size: int
    perms: str
    offset:int
    objfile: str


class Mappings:
    def __init__(self):
        mappings = gdb.execute('info proc mappings', to_string=True).split('\n')
        mappings = [i.strip() for i in mappings[3:] if i.strip()]
        headers = [i.strip() for i in mappings[0].split('  ') if i.strip()]
        self.values = []
        for mapping in mappings[1:]:
            d = {k : v for k, v in zip(headers, mapping.split())}
            self.values.append(Mapping(
                int(d['Start Addr'], 16),
                int(d['End Addr'], 16),
                int(d['Size'], 16),
                d.get('Perms'),
                d.get('Offset'),
                d.get('objfile')))

    def writeable(self) -> list[Mapping]:
        return [i for i in self.values if 'w' in i.perms]


###########################################################
# Value getters in a function call
###########################################################

class ConstVal:
    def __init__(self, v):
        self.v = v

    def get(self, stackFrame):
        return self.v

class FunctionArgVal:
    def __init__(self, n:int):
        assert n <= 6
        self.n = n - 1
        self.regs = ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9']

    def get(self, stackFrame):
        assert stackFrame.architecture().name() == 'i386:x86-64'
        return stackFrame.read_register(self.regs[self.n])


###########################################################
# Breakpoint handlers
###########################################################

class ValueCatcher(gdb.Breakpoint):
    def __init__(self, buf_arg, size_arg, *args):
        super().__init__(*args)
        self.values = []
        self.buf_arg = buf_arg
        self.size_arg = size_arg

    def stop(self):
        fr = gdb.selected_frame()
        inbuf = self.buf_arg.get(fr).cast(gdb.lookup_type('uint8_t').pointer())
        insize = self.size_arg.get(fr)
        v = bytes(int(inbuf[i]) for i in range(insize))
        print('Captured value:', v)
        self.values.append(v)

        return False


class ValueSearcher(gdb.Breakpoint):
    def __init__(self, values, *args):
        super().__init__(*args)
        self.values = values
        self.mappings = None

    def stop(self):
        fr = gdb.selected_frame()

        if self.mappings is None:
            self.mappings = Mappings()

        inferior = gdb.selected_inferior()
        for m in self.mappings.writeable():
            for v in self.values:
                addr = inferior.search_memory(m.start_addr, m.size, v)
                if addr is not None:
                    print('Found value:', v, 'at', hex(addr), m.objfile)
        return False


###########################################################
# Main setup
###########################################################

c_key = ValueCatcher(FunctionArgVal(4), ConstVal(16), 'EVP_EncryptInit_ex')
ValueSearcher(c_key.values, 'hexdump')

c_pt = ValueCatcher(FunctionArgVal(4), FunctionArgVal(5), 'EVP_EncryptUpdate')
ValueSearcher(c_pt.values, 'hexdump')


gdb.execute("run")
if len(c_key.values) == 0 and len(c_pt.values) == 0:
    print("No values captured, did capture points get optimized out?")
gdb.execute("quit")


# Expected output is like this:
# Captured value: b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10'
# Captured value: b'something something'
# Found value: b'something something' at 0x7fffffffdb50 [stack]

# Will catch key in OpenSSL context if EVP_CIPHER_CTX_free is not called
