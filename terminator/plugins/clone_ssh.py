import functools
import subprocess

import gtk

from terminatorlib import config
from terminatorlib import plugin
from terminatorlib import terminal
from terminatorlib import terminator
from terminatorlib import version


AVAILABLE = ['CloneSSH']


class CloneSSH(plugin.MenuItem):

    def __init__(self):
        super(CloneSSH, self).__init__()
        self.patch_keybindings()
        self.patch_terminal()

    def patch_keybindings(self):
        keybindings = terminator.Terminator().keybindings
        keybindings.keys['clone_horiz'] = '<Alt><Ctrl>o'
        keybindings.keys['clone_vert'] = '<Alt><Ctrl>e'
        keybindings.configure(keybindings.keys)

    def patch_terminal(self):
        terminal.Terminal.key_clone_horiz = lambda s: self.clone_horiz(s)
        terminal.Terminal.key_clone_vert = lambda s: self.clone_vert(s)

    def callback(self, menuitems, menu, terminal):
        for name, abbrev in [('Horizontally', self.clone_horiz),
                             ('Vertically', self.clone_vert)]:
            item = gtk.MenuItem('Clone %s' % name)
            item.connect('activate', lambda widget, cwd: func(terminal))
            menuitems.append(item)

    def clone_horiz(self, terminal):
        self.clone_prepare(terminal)
        terminal.emit('split-horiz', terminal.terminator.pid_cwd(terminal.pid))

    def clone_vert(self, terminal):
        self.clone_prepare(terminal)
        terminal.emit('split-vert', terminal.terminator.pid_cwd(terminal.pid))

    def clone_prepare(self, terminal):
        cmds = [
            # exec ssh ... case
            ['ps', '--pid', str(terminal.pid), '-o', 'command'],
            # ssh ... case
            ['ps', '--ppid', str(terminal.pid), '-o', 'command']]
        for cmd in cmds:
            try:
                for candidate in subprocess.check_output(cmd).splitlines():
                    candidate = candidate.strip()
                    if candidate.startswith('ssh '):
                        config.Config().options_get().command = candidate
            except subprocess.CalledProcessError:
                pass
