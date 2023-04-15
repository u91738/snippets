#!/bin/bash
set -e

echo '#####################################################'
echo '# memcpy to stack with variable size'
echo '#####################################################'

weggli '
    _ $f(_ $size) {
        _ $buf[_];
        NOT: if( _($size) ) { }
        memcpy($buf, _, $size);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg.$size_field) ) { }
        memcpy($buf, _, $size_arg.$size_field);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg->$size_field) ) { }
        memcpy($buf, _, $size_arg->$size_field);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg->$size_field) ) { }
        $tmp = $size_arg->$size_field;
        NOT: if( _($size_arg->$size_field) ) { }
        NOT: if( _($tmp) ) { }
        memcpy($buf, _, $tmp);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg.$size_field) ) { }
        $tmp = $size_arg.$size_field;
        NOT: if( _($size_arg.$size_field) ) { }
        NOT: if( _($tmp) ) { }
        memcpy($buf, _, $tmp);
    }' .
