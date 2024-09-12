source $VIMRUNTIME/defaults.vim



set nocompatible              " be iMproved, required
filetype off                  " required

call plug#begin()

" List your plugins here
Plug 'catppuccin/vim', { 'as': 'catppuccin' }
Plug 'vim-airline/vim-airline'

call plug#end()

filetype plugin indent on    " required

set hls
set is
set cb=unnamed
set ts=4
set sw=4
set si
set guifont=Cascadia\ Code\ Bold\ 16
set shell=/usr/bin/fish
let g:airline_theme = 'catppuccin_mocha'

nnoremap <C-A> ggVG
inoremap { {}<Left>
inoremap {<CR> {<CR>}<Esc>O
inoremap {{ {
inoremap {} {}
cnoremap sudow :w !sudo tee % >/dev/null
:imap ii <Esc>

set nu
augroup numbertoggle
    autocmd!
    autocmd BufEnter,FocusGained,InsertLeave * set rnu
    autocmd BufLeave,FocusLost,InsertEnter * set nornu
augroup END
