let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
doautoall SessionLoadPre
silent only
silent tabonly
cd ~/github/LuStCodeSnippets
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
set shortmess+=aoO
badd +1 ~/github/LuStCodeSnippets
badd +190 LuStCodeSnippets_sh/utils.sh
badd +52 term://~/github/LuStCodeSnippets//130856:/bin/bash
badd +20 term://~/github/LuStCodeSnippets//133196:/bin/bash
argglobal
%argdel
$argadd ~/github/LuStCodeSnippets
edit LuStCodeSnippets_sh/utils.sh
argglobal
setlocal foldmethod=indent
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=2
setlocal foldminlines=1
setlocal foldnestmax=5
setlocal foldenable
4
sil! normal! zo
5
sil! normal! zo
18
sil! normal! zo
25
sil! normal! zo
30
sil! normal! zo
4
sil! normal! zc
70
sil! normal! zo
71
sil! normal! zo
71
sil! normal! zc
70
sil! normal! zc
134
sil! normal! zo
135
sil! normal! zo
144
sil! normal! zo
144
sil! normal! zc
135
sil! normal! zc
167
sil! normal! zc
172
sil! normal! zo
172
sil! normal! zc
186
sil! normal! zo
186
sil! normal! zc
191
sil! normal! zc
194
sil! normal! zc
let s:l = 191 - ((190 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 191
normal! 03|
lcd ~/github/LuStCodeSnippets
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
