#!/bin/bash
set -e

weggli '
    _ $f(_ $size) {
        _ $buf[_];
        NOT: if( _($size) ) { }
        read(_, $buf, $size);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg.$size_field) ) { }
        read( _, $buf, $size_arg.$size_field);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg->$size_field) ) { }
        read(_, $buf, $size_arg->$size_field);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg->$size_field) ) { }
        $tmp = $size_arg->$size_field;
        NOT: if( _($size_arg->$size_field) ) { }
        NOT: if( _($tmp) ) { }
        read(_, $buf, $tmp);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg.$size_field) ) { }
        $tmp = $size_arg.$size_field;
        NOT: if( _($size_arg.$size_field) ) { }
        NOT: if( _($tmp) ) { }
        read(_, $buf, $tmp);
    }' .




weggli '
    _ $f(_ $size) {
        _ $buf[_];
        NOT: if( _($size) ) { }
        fread($buf, $size, _);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg.$size_field) ) { }
        fread($buf, $size_arg.$size_field, _);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg->$size_field) ) { }
        fread($buf, $size_arg->$size_field, _);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg->$size_field) ) { }
        $tmp = $size_arg->$size_field;
        NOT: if( _($size_arg->$size_field) ) { }
        NOT: if( _($tmp) ) { }
        fread($buf, $tmp, _);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg.$size_field) ) { }
        $tmp = $size_arg.$size_field;
        NOT: if( _($size_arg.$size_field) ) { }
        NOT: if( _($tmp) ) { }
        fread($buf, $tmp, _);
    }' .




weggli '
    _ $f(_ $size) {
        _ $buf[_];
        NOT: if( _($size) ) { }
        fread($buf, _, $size, _);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg.$size_field) ) { }
        fread($buf, _, $size_arg.$size_field, _);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg->$size_field) ) { }
        fread($buf, _, $size_arg->$size_field, _);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg->$size_field) ) { }
        $tmp = $size_arg->$size_field;
        NOT: if( _($size_arg->$size_field) ) { }
        NOT: if( _($tmp) ) { }
        fread($buf, _, $tmp, _);
    }' .

weggli '
    _ $f(_ $size_arg) {
        _ $buf[_];
        NOT: if( _($size_arg.$size_field) ) { }
        $tmp = $size_arg.$size_field;
        NOT: if( _($size_arg.$size_field) ) { }
        NOT: if( _($tmp) ) { }
        fread($buf, _, $tmp, _);
    }' .