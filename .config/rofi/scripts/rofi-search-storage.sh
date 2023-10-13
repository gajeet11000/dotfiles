opener="xdg-open"

selection=$(fd . --hidden /mnt/Ajeet 2>/dev/null | \
    rofi -sort -sorting-method fzf -dmenu -i -theme ./themes/search -no-custom -p "Search:" | \
    sed 's/ /\\ /g'
)

eval $opener "$selection"