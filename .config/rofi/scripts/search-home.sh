#!/bin/bash

opener="xdg-open"

if [[ -z "$1" ]]; then
    fd . --hidden $HOME 2>/dev/null | sed "s;$HOME;~;g"
else
    selection=$(echo "$1" | sed 's;\~;$HOME; ;s/ /\\ /g; s/\&/\\&/g; s/(/\\(/g; s/)/\\)/g')
    eval $opener "$selection" > /dev/null 2>&1 &
fi