#!/bin/bash
set -e

echo '#####################################################'
echo '# Uninitialized pointer'
echo '#####################################################'
weggli $WEGGLI_ARGS '{
    _* $p;
    NOT: $p = _;
    NOT: &$p;
    $func($p);
}'
