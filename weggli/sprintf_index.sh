#!/bin/bash
set -e

echo '#####################################################'
echo '# Result of *printf indexes an array'
echo '#####################################################'

weggli $WEGGLI_ARGS -R '$fn=^[^n]*printf' '{
    $ret = $fn($b,_,_);
    NOT: if(_($ret)) { }
    _[$ret] = _;
}' .
