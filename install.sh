#!/usr/bin/bash

sudo pacman -Syyu

sudo pacman --needed --noconfirm -S - < pkglist.txt

yay -Syyu

yay --needed --noconfirm -S - < aur.txt

git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
