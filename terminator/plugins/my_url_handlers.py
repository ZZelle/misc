import re
from  terminatorlib import plugin


AVAILABLE = ['OpenStackURLHandler']


class OpenStackURLHandler(plugin.URLHandler):
    handler_name = 'os-launchpad-url'
    match = r'\b(Closes|Partial|Related)-Bug:?\s?#?\d+\b'

    def callback(self, url):
        print '#' * 150
        item = re.search('r[^\d](\d+)$', url).group(0)
        return 'https://bugs.launchpad.net/bugs/%s' % item
