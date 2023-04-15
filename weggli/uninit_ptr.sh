#!/bin/bash
set -e

echo '#####################################################'
echo '# Uninitialized pointer'
echo '#####################################################'
weggli '{
    _* $p;
    NOT: $p = _;
    NOT: &$p;
    $func($p);
}'
