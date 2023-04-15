#!/bin/bash
set -e

echo '#####################################################'
echo '# Allocation with potential underflow'
echo '#####################################################'

weggli -R '$fn=lloc' -R '$a=[a-z]' -R '$b=[a-z]' '{
    not: _ * a;
    not: _ * b;
    $x = $fn(_($a)-_($b));
    not: if(_($x)) { }
}' .

weggli -R '$fn=lloc' -R '$a=[a-z]' -R '$b=[a-z]' '{
    not: _ * a;
    not: _ * b;
    $size=_($a)-_($b);
    $x = $fn($size);
    not: if(_($x)) { }
}' .
