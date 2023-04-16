#!/bin/bash
set -e

echo '#####################################################'
echo '# Integer overflow'
echo '#####################################################'
weggli $WEGGLI_ARGS -R '$f=atoi|strto[uql]' '{ $user_num = $f(_); $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=atoi|strto[uql]' '{ $user_num = $f(_); $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=atoi|strto[uql]' '{ $user_num = $f(_); $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=atoi|strto[uql]' '{ $user_num = $f(_); _ - $user_num; }' .

weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, &$user_num);                $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, &$user_num);             $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num);          $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num);          $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, &$user_num);       $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, _, &$user_num);    $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, &$user_num, _);             $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, &$user_num, _);          $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num, _);       $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num, _);       $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, &$user_num, _);    $user_num + _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, _, &$user_num, _); $user_num + _; }' .

weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, &$user_num);                $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, &$user_num);             $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num);          $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num);          $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, &$user_num);       $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, _, &$user_num);    $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, &$user_num, _);             $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, &$user_num, _);          $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num, _);       $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num, _);       $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, &$user_num, _);    $user_num * _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, _, &$user_num, _); $user_num * _; }' .

weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, &$user_num);                $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, &$user_num);             $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num);          $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num);          $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, &$user_num);       $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, _, &$user_num);    $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, &$user_num, _);             $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, &$user_num, _);          $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num, _);       $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num, _);       $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, &$user_num, _);    $user_num - _; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, _, &$user_num, _); $user_num - _; }' .

weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, &$user_num);                _ - $user_num; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, &$user_num);             _ - $user_num; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num);          _ - $user_num; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num);          _ - $user_num; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, &$user_num);       _ - $user_num; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, _, &$user_num);    _ - $user_num; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, &$user_num, _);             _ - $user_num; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, &$user_num, _);          _ - $user_num; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num, _);       _ - $user_num; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, &$user_num, _);       _ - $user_num; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, &$user_num, _);    _ - $user_num; }' .
weggli $WEGGLI_ARGS -R '$f=scanf' '{ $f(_, _, _, _, _, &$user_num, _); _ - $user_num; }' .
