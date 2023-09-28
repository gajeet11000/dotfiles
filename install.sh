#!/usr/bin/bash

sudo pacman -Syyu

sudo pacman --needed --noconfirm -S - < pkglist.txt

yay --needed --noconfirm -S - < aur.txt

chsh -s /bin/fish
sudo chsh -s /bin/fish

git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

git clone https://github.com/vinceliuice/Tela-circle-icon-theme.git
cd Tela-circle-icon-theme
./install.sh dracula

echo "Xcursor.theme: Bibata-Rainbow-Modern" >> ~/.Xresources