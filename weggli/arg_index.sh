#!/bin/bash
set -e

echo '#####################################################'
echo '# Stack array indexed with func argument'
echo '#####################################################'

weggli '
    _ $fn(_ $limit) {
        _ $buf[_];
        not: if( _($limit) ) { _ ; }

        for (_; _($limit); _($i)) {
            $buf[$i]=_;
        }
    }' .

weggli '
    _ $fn(_ $limit_arg) {
        _ $buf[_];
        not: if( _($limit_arg->field) ) { _ ; }

        for (_; _($limit_arg->field); _($i)) {
            $buf[$i]=_;
        }
    }' .

weggli '
    _ $fn(_ $limit_arg) {
        _ $buf[_];
        not: if( _($limit_arg.field) ) { _ ; }

        for (_; _($limit_arg.field); _($i)) {
            $buf[$i]=_;
        }
    }' .

weggli '
    _ $fn(_ $limit) {
        _ $buf[_];
        not: if( _($limit) ) { _ ; }

        while (_($limit)) {
            not: for(_;_;_)
            not: while(_) { }
            $buf[$i]=_;
        }
    }' .

weggli '
    _ $fn(_ $limit_arg) {
        _ $buf[_];
        not: if( _($limit_arg->$field) ) { _ ; }

        while (_($limit_arg->$field)) {
            not: for(_;_;_)
            not: while(_) { }
            $buf[$i]=_;
        }
    }' .

weggli '
    _ $fn(_ $limit_arg) {
        _ $buf[_];
        not: if( _($limit_arg.$field) ) { _ ; }

        while (_($limit_arg.$field)) {
            not: for(_;_;_)
            not: while(_) { }
            $buf[$i]=_;
        }
    }' .
