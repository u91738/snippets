#!/bin/bash
set -e

echo '#####################################################'
echo '# scanf result not checked'
echo '#####################################################'

weggli $WEGGLI_ARGS -R '$fn=^v?f?scanf' '{ strict: $fn(_); }' .
weggli $WEGGLI_ARGS -R '$fn=sscanf' -R 's=[a-z]' '{ strict: $fn($s, _); }' .
