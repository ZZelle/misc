import gtk

from terminatorlib import config
from terminatorlib import plugin
from terminatorlib import prefseditor
from terminatorlib import terminal
from terminatorlib import terminator


AVAILABLE = ['FlipColors']


class FlipColors(plugin.MenuItem):

    def __init__(self):
        super(FlipColors, self).__init__()
        self.config = config.Config()
        self.patch_keybindings()
        self.patch_terminal()

    def patch_keybindings(self):
        keybindings = terminator.Terminator().keybindings
        keybindings.keys['flip_colors'] = '<Alt><Ctrl>f'
        keybindings.configure(keybindings.keys)

        prefseditor.PrefsEditor.keybindingnames.update(
            flip_colors='Flip colors')

    def patch_terminal(self):
        terminal.Terminal.key_flip_colors = self.flip

    def callback(self, menuitems, menu, terminal):
        item = gtk.MenuItem('Flip colors')
        item.connect('activate', self.flip)
        menuitems.append(item)

    def flip(self, dontcare=None):
        if self.config['background_darkness'] < .9:
            self.config['background_darkness'] = .9
            self.config['foreground_color'] = "#ffffff"
        else:
            self.config['background_darkness'] = .1
            self.config['foreground_color'] = "#e53c00"
        self.config.save()
        terminator.Terminator().reconfigure()
