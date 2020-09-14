if exists('g:my')
    finish
endif

let g:my = 0


" rnu/nu/none toggle.
command! NumberToggle :call s:NumberToggle()
function! s:NumberToggle()
    if !&nu
        set nu
        set rnu
    elseif &rnu
        set nornu
    else
        set nonu
    endif
endfunction


" Zoom/unzoom toggle.
command! ZoomToggle :call s:ZoomToggle()
function! s:ZoomToggle()
    if exists('t:unzoom')
        execute t:unzoom
        unlet t:unzoom
    else
        let t:unzoom = winrestcmd()
        resize
        vertical resize
    endif
endfunction


command! EditTest :call _EditTest()
function! _EditTest()
pythonx << endpython
import os.path, vim
name = vim.eval("expand('%:t')")
if name.endswith('.py'):
    path = vim.eval("expand('%:h')").split('/')
    if name.startswith('test_'):
        for cursor in "tests", "unit":
            if cursor in path:
                path.remove(cursor)
        path.append(name[5:])
    else:
        path.insert(1, "tests")
        if os.path.isdir("%s/tests/unit" % path[0]):
            path.insert(2, "unit")
        path.append('test_%s' % name)

    path = '/'.join(path)
    if os.path.exists(path):
        vim.command('edit %s' % path)
endpython
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


command! -nargs=1 -complete=custom,_PuppetModuleComplete PuppetModule :call _PuppetModule(<f-args>)
function! _PuppetModule(module)
pythonx << endpython
import os, vim
module = vim.eval("a:module")
splitteds = [x for x in module.split(':') if x]
splitteds.insert(0, 'modules')
splitteds.insert(2, 'manifests')
path = os.path.join(*splitteds) + '.pp'
if os.path.exists(path):
    vim.command('edit %s' % path)
else:
    print("Failed to load module %s" % module)
endpython
endfunction

function! _PuppetModuleComplete(module, line, pos)
pythonx << endpython
import os, vim
module = vim.eval("a:module")
splitteds = module.split('::')
if len(splitteds) == 1:
    folder = 'modules'
    prefix = ''.join(splitteds)
elif splitteds[-1]:
    folder = os.path.join('modules', splitteds[0], 'manifests', *splitteds[1:-1])
    prefix = splitteds[-1]
else:
    folder = os.path.join('modules', splitteds[0], 'manifests', *splitteds[1:])
    prefix = ''
try:
    package = module.rstrip(prefix)
    _, subfolders, files = os.walk(folder).next()
    modules = [x[:-3] for x in files if x.endswith('.pp')]
    candidates = sorted('%s%s' % (package, x) for x in modules if x.startswith(prefix))
    candidates += sorted('%s%s::' % (package, x) for x in subfolders if x.startswith(prefix))
    vim.command("return '%s'" % "\n".join(candidates))
except:
    pass
endpython
endfunction
