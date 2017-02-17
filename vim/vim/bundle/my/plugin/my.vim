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


command! EditTest :call _EditTest()
function! _EditTest()
    let file_name = expand('%:t')

    if file_name =~ '\.py$'
        let paths = split(expand('%:h'), '/')
        if file_name !~ '^test_'
            call extend(paths, ['tests', 'unit'], 1)
            call add(paths, 'test_' . file_name)
        else
            call remove(paths, 1, 2)
            call add(paths, file_name[5:])
        endif

        let peer_name = join(paths, '/')
        if filereadable(peer_name)
            exec 'edit ' peer_name
        endif
    endif
endfunction


command! -nargs=? GGref :call _GGref(<f-args>)
function! _GGref(...)
    if a:0 == 0
        let g:gitgutter_diff_base = ''
    else
        let g:gitgutter_diff_base = a:1
    endif
    GitGutterAll
endfunction


command! -nargs=? GGargs :call _GGref(<f-args>)
function! _GGref(...)
    if a:0 == 0
        let g:gitgutter_diff_args = ''
    else
        let g:gitgutter_diff_args = join(a:000, " ")
    endif
    GitGutterAll
endfunction
