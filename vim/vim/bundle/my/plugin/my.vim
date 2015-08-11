if exists('g:my')
    finish
endif

let g:my = 0

command! NumberToggle :call _NumberToggle()
function! _NumberToggle()
    if !&nu
        set nu
        set rnu
    elseif &rnu
        set nornu
    else
        set nonu
    endif
endfunction
