sudo pacman -Syyy

sudo pacman -Syu

sudo pacman -S --noconfirm base-devel

pamac build safeeyes
pamac build teamviewer
pamac build fisher 
pamac build gammy postman-bin heroku-cli

sudo pacman -S --noconfirm firefox gimp telegram-desktop mpv pamac-flatpak-plugin pamac-cli pamac-gtk pamac-snap-plugin xfce4-netload-plugin rofi gvim gcc gnome-disk-utility mintstick moc cowsay fortune-mod cmatrix lolcat otf-cascadia-code deluge-gtk xorg-xbacklight gnome-calculator asciiquarium jre-openjdk jre-openjdk-headless fish nomacs xournalpp bitwarden pinta lsd

cp -r .config/ .fonts/ .icons/ .moc/ .themes/ .vim/ .local/ .xdman/ .gvimrc .vimrc .bashrc ~/

sudo pacman -R --noconfirm blueman midori parole mousepad

sudo chsh -s /usr/bin/fish
chsh -s /usr/bin/fish

fisher install IlanCosman/tide

cd /home/gajeet/Documents/

git clone https://github.com/gajeet11000/Apna-College-DSA-Practice-Questions.git

sudo mount /dev/sda4 /mnt/Ajeet/

sudo sh /mnt/Ajeet/SOFTWARE/Linux\ Softwares/xdm-setup-7.2.11/install.sh
