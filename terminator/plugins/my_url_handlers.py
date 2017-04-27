from terminatorlib import plugin


class JiraURLHandler(plugin.URLHandler):
    handler_name = 'pegjira-url'
    nameopen = "Open PegJira"
    namecopy = "Copy PegJira link"
    match = r'\<COMC-[0-9]+'

    def callback(self, url):
        return 'http://pegjira.pegasus.theresis.org/browse/%s' % url


AVAILABLE = [JiraURLHandler.__name__]
