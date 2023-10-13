set -U fish_greeting
alias c="clear"
alias aq="asciiquarium"
alias cm="cmatrix"
alias cs="fortune | cowsay | lolcat"
alias ls="lsd -a"

fish_vi_key_bindings
bind -M insert -m default ii backward-char force-repaint