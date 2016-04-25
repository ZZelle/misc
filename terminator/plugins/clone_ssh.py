import functools
import subprocess

import gtk

from terminatorlib import config
from terminatorlib import plugin
from terminatorlib import prefseditor
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

        prefseditor.PrefsEditor.keybindingnames.update(
            clone_horiz='Clone horizontally',
            clone_vert='Clone vertically')

    def patch_terminal(self):
        terminal.Terminal.key_clone_horiz = lambda s: self.clone_horiz(s)
        terminal.Terminal.key_clone_vert = lambda s: self.clone_vert(s)

    def callback(self, menuitems, menu, terminal):
        item = gtk.MenuItem('Clone Horizontally')
        item.connect('activate', lambda widget: self.clone_horiz(terminal))
        menuitems.append(item)
        item = gtk.MenuItem('Clone Vertically')
        item.connect('activate', lambda widget: self.clone_vert(terminal))
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
                        if ' -W' not in candidate:
                            # -W is commonly used in ssh ProxyCommand
                            config.Config().options_get().command = candidate
            except subprocess.CalledProcessError:
                pass
