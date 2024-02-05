#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}


#Find out your monitor name with xrandr or arandr (save and you get this line)
#xrandr --output VGA-1 --primary --mode 1360x768 --pos 0x0 --rotate normal
#xrandr --output DP2 --primary --mode 1920x1080 --rate 60.00 --output LVDS1 --off &
#xrandr --output LVDS1 --mode 1366x768 --output DP3 --mode 1920x1080 --right-of LVDS1
#xrandr --output HDMI2 --mode 1920x1080 --pos 1920x0 --rotate normal --output HDMI1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output VIRTUAL1 --off
#autorandr horizontal

#Some ways to set your wallpaper besides variety or nitrogen
# feh --bg-fill /usr/share/backgrounds/archlinux/arch-wallpaper.jpg &
# feh --bg-fill /usr/share/backgrounds/arcolinux/arco-wallpaper.jpg &
#wallpaper for other Arch based systems

if [ $# -ne 2 ]; then
    echo "Usage: $0 <argument1> <argument2>"
    exit 1
fi


wallpapers_path="${1}"
lockscreen_wallpapers_path="${2}"

betterlockscreen -u "$lockscreen_wallpapers_path" &

# Run feh command with modified path
feh --bg-fill -z "$wallpapers_path" &

if [[ ! `pidof xfce-polkit` ]]; then
	/usr/lib/xfce-polkit/xfce-polkit &
fi

exec dunst &
exec thunar --daemon &
xfsettingsd &
run nm-applet &
run xfce4-power-manager &
run numlockx on &
blueman-applet &

picom --config $HOME/.config/picom/picom.conf &

#starting user applications at boot time
run copyq &
run volumeicon &
run flameshot &
run kdeconnect-indicator &
