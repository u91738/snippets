#!/bin/bash
set -e

echo '#####################################################'
echo '# memcpy/strncpy with potential underflow'
echo '#####################################################'
weggli -R 'func=.*[mn]cpy$' -R 'm=[a-z]' -R 'n=[a-z]' '{$func(_, _, $n - $m);}' .