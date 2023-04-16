#!/bin/bash
set -e

# when fiddling with weggli you might want to
# export WEGGLI_ARGS='--cpp --exclude=...'

echo '#####################################################'
echo '# Allocation with potential underflow'
echo '#####################################################'

weggli $WEGGLI_ARGS -R '$fn=lloc' -R '$a=[a-z]' -R '$b=[a-z]' '{
    not: _ * a;
    not: _ * b;
    $x = $fn(_($a)-_($b));
    not: if(_($x)) { }
}' .

weggli $WEGGLI_ARGS -R '$fn=lloc' -R '$a=[a-z]' -R '$b=[a-z]' '{
    not: _ * a;
    not: _ * b;
    $size=_($a)-_($b);
    $x = $fn($size);
    not: if(_($x)) { }
}' .
