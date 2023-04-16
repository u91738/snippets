#!/bin/bash
set -e

# This one is pretty bad, will report
# if(...) { free(a); } else { f(a); }

echo '#####################################################'
echo '# Use after free'
echo '#####################################################'
weggli $WEGGLI_ARGS '{
    free($a);
    not: $a=_;
    not: return _;
    not: return;
    not: continue;
    not: break;
    not: goto _;
    _($a);
}' .
