#!/bin/bash

opener="kitty"

if [[ -z "$1" ]]; then
    fd . --hidden --type d / --exclude /home --exclude /mnt --exclude /lost+found --exclude /root 2>/dev/null
else
    selection=$(echo "$1" | sed 's/ /\\ /g; s/\&/\\&/g; s/(/\\(/g; s/)/\\)/g')
    eval $opener "$selection" > /dev/null 2>&1 &
fi