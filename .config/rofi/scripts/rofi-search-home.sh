opener="xdg-open"

selection=$(fd . --hidden $HOME 2>/dev/null | \
    sed 's;$HOME;~;' | \
    rofi -sort -sorting-method fzf -dmenu -i -theme ./themes/search -no-custom -p "Search:" | \
    sed 's;\~;$HOME; ;s/ /\\ /g; s/\&/\\&/g; s/(/\\(/g; s/)/\\)/g'
)
eval $opener "$selection" 