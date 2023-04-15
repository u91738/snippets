#!/bin/bash
set -e

echo '#####################################################'
echo '# scanf result not checked'
echo '#####################################################'

weggli -R '$fn=^v?f?scanf' '{ strict: $fn(_); }' .
weggli -R '$fn=sscanf' -R 's=[a-z]' '{ strict: $fn($s, _); }' .
