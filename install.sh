sudo pacman -Syyy

sudo pacman -Syu

sudo pacman -S --noconfirm base-devel

pamac build safeeyes
pamac build teamviewer
pamac build gammy

sudo pacman -S --noconfirm firefox gimp telegram-desktop mpv xfce4-netload-plugin rofi gvim gcc gnome-disk-utility mintstick moc cowsay fortune-mod cmatrix lolcat otf-cascadia-code deluge-gtk xorg-xbacklight gnome-calculator asciiquarium fish nomacs xournalpp bitwarden pinta lsd skippy-xd nemo nemo-engrampa fisher yay dconf-editor flameshot

cp -r .config/ .fonts/ .icons/ .moc/ .themes/ .vim/ .local/ .xdman/ .gvimrc .vimrc .bashrc ~/

sudo pacman -R --noconfirm blueman midori parole mousepad

sudo chsh -s /usr/bin/fish
chsh -s /usr/bin/fish

fisher install IlanCosman/tide
