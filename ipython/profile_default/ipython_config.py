try:
    c
except NameError:
    # NOTE(cby): Support older iPython versions
    c = get_config()
c.TerminalIPythonApp.display_banner = False
c.InteractiveShell.autocall = 2
c.InteractiveShell.show_rewritten_input = False
c.TerminalInteractiveShell.confirm_exit = False
