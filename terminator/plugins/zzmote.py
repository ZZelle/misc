#!/usr/bin/env python

import argparse

import dbus


NAME = 'org.zzelle.terminator'
PATH = '/' + '/'.join(NAME.split('.'))

class Proxy():
    def __init__(self):
        try:
            self.proxy = dbus.SessionBus().get_object(NAME, PATH)
            self.set_target()
        except dbus.exceptions.DBusException:
            print 'Failed to contact Terminator'
            raise SystemExit(1)

    def list_terms(self):
        print '\n'.join(self.proxy.list_terms())

    def get_term(self):
        print self.proxy.get_term()

    def set_target(self, uuid=0):
        self.uuid = uuid

    def hsplit_term(self):
        print self.proxy.hsplit_term(self.uuid)

    def vsplit_term(self):
        print self.proxy.vsplit_term(self.uuid)

    def run_term(self, command, *args):
        self.proxy.run_term(command, self.uuid)

    def clear_term(self):
        self.proxy.clear_term(self.uuid)


class FuncAction(argparse.Action):
    def __init__(self, option_strings, func=None, nargs=0, **kwargs):
        if not callable(func):
            raise ValueError('func must be callable')
        self.func = func
        super(FuncAction, self).__init__(option_strings, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        funcs = argparse._ensure_value(namespace, self.dest, [])
        funcs.append((self.func, values))


def main():
    proxy = Proxy()
    parser = argparse.ArgumentParser()
    add_arg = lambda *args, **kwargs: parser.add_argument(*args, dest='funcs', action=FuncAction, **kwargs)
    add_arg('-l', '--list', func=proxy.list_terms)
    add_arg('-g', '--get', func=proxy.get_term)
    add_arg('-u', '--uuid', func=proxy.set_target, nargs=1)
    add_arg('-U', '--nouuid', func=proxy.set_target)
    add_arg('-o', '--hori', func=proxy.hsplit_term)
    add_arg('-e', '--vert', func=proxy.vsplit_term)
    add_arg('-c', '--clear', func=proxy.clear_term)
    add_arg('-r', '--run', func=proxy.run_term, nargs=1)
    add_arg('-s', '--RUN', func=proxy.run_term, nargs=argparse.REMAINDER)

    options = parser.parse_args()
    for func, args in getattr(options, 'funcs', []):
        func(*args)


if __name__ != '__main__':
    import dbus.glib
    import dbus.service

    dbus.glib.threads_init()

    from terminatorlib import plugin
    from terminatorlib import terminator


    AVAILABLE = ['ZZmote']
    class ZZmote(dbus.service.Object, plugin.Plugin):
        capabilities = ['ZZmote']

        def __init__(self):
            busname = dbus.service.BusName(NAME, bus=dbus.SessionBus())
            super(ZZmote, self).__init__(busname, PATH)
            self._terminator = terminator.Terminator()

        @dbus.service.method(NAME)
        def list_terms(self):
            return [t.uuid.urn for t in self._terminator.terminals]

        @dbus.service.method(NAME)
        def get_term(self):
            return self._term().uuid.urn

        @dbus.service.method(NAME)
        def hsplit_term(self, uuid=None):
            self._term(uuid).key_split_horiz()
            return self._last

        @dbus.service.method(NAME)
        def vsplit_term(self, uuid=None):
            self._term(uuid).key_split_vert()
            return self._last

        @dbus.service.method(NAME)
        def run_term(self, command, uuid=None):
            command = str(command).rstrip() + '\n'
            self._term(uuid).feed(command)

        @dbus.service.method(NAME)
        def clear_term(self, uuid=None):
            self._term(uuid).key_reset_clear()


        @dbus.service.method(NAME)
        def add_tab(self):
            self._window.tab_new(self._window.get_focussed_terminal())
            return self._last


        def _term(self, uuid=None):
            if uuid:
                return self._terminator.find_terminal_by_uuid(uuid)
            return self._window.get_focussed_terminal()

        @property
        def _last(self):
            return self._terminator.terminals[-1].uuid.urn

        @property
        def _window(self):
            # Works only with one window !
            # Interesting: terminatorlib.terminal:776
            return self._terminator.windows[0]
else:
    main()
