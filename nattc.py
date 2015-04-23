#!/usr/bin/env python
# Based on http://linux.programdevelop.com//2898840/

import abc
import collections
import re
import subprocess


_RE_FIND_FILTER = re.compile('filter u32 fh (\S+::\S+) ')
_RE_FIND_INGRESS = re.compile(
    'action order \d+:  nat ingress (?P<fip>\S+)/32 (?P<ip>\S+) ')
_RE_FIND_EGRESS = re.compile(
    'action order \d+:  nat egress (?P<ip>\S+)/32 (?P<fip>\S+) ')


def parse_filter_show_result(rawdata, action_finder):
    data = collections.defaultdict(list)
    filter_id = None
    for line in rawdata.splitlines():
        match = _RE_FIND_FILTER.search(line)
        if match:
            filter_id = match.group(1)
            continue

        match = action_finder.match(line.lstrip())
        if match and filter_id:
            floating_ip = match.group('fip')
            fixed_ip = match.group('ip')
            data[floating_ip, fixed_ip].append(filter_id)

    return dict(data)


class OneDirectionNat(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, interface, classid, action_finder):
        self.interface = interface
        self.action_finder = action_finder
        self.classid = classid
        self.ensured_qdisc = False

    def ensure_qdisc(self):
        if not self.ensured_qdisc:
            self._ensure_qdisc()
        self.ensured_qdisc = True

    @abc.abstractmethod
    def _ensure_qdisc(self):
        pass

    @abc.abstractmethod
    def create_nat(self, floating_ip, fixed_ip):
        pass

    def list_nat_filters(self):
        rawdata = self._manage_filter('show', [])
        return parse_filter_show_result(rawdata, self.action_finder)

    def update_nats(self, nats):
        self.ensure_qdisc()

        current_nat_filters = self.list_nat_filters()

        for nat, filter_ids in current_nat_filters.items():
            if nat not in nats:
                # Remove obsolete nat filters
                for filter_id in filter_ids:
                    self.delete_filter(filter_id)
            elif len(filter_ids) > 1:
                # Remove directional nat filter duplicates
                for filter_id in filter_ids[1:]:
                    self.delete_filter(filter_id)

        for nat in nats:
            if nat not in current_nat_filters:
                # Create directional nat filter
                self.create_nat(*nat)

    def delete_filter(self, filter_id):
        self._manage_filter('del', ['handle', filter_id, 'u32'])

    def _ensure_qdisc(self, args):
        cmd = ['tc', 'qdisc', 'add', 'dev', self.interface] + args
        return subprocess.call(cmd) in [0, 2]

    def _manage_filter(self, action, args):
        cmd = [
            'tc', 'filter', action, 'dev', self.interface,
            'parent', self.classid, 'protocol', 'ip', 'pref', '10'] + args
        return subprocess.check_output(cmd)


class IngressNat(OneDirectionNat):

    def __init__(self, interface):
        super(IngressNat, self).__init__(interface, 'ffff:', _RE_FIND_INGRESS)

    def _ensure_qdisc(self):
        args = ['ingress', 'handle', self.classid]
        self._ensure_qdisc(args)

    def create_nat(self, floating_ip, fixed_ip):
        floating_ip = '%s/32' % floating_ip
        args = [
            'u32', 'match', 'ip', 'dst', floating_ip,
            'action', 'nat', 'ingress', floating_ip, fixed_ip]
        self._manage_filter('add', args)


class EgressNat(OneDirectionNat):

    def __init__(self, interface):
        super(EgressNat, self).__init__(interface, '10:', _RE_FIND_EGRESS)

    def _ensure_qdisc(self):
        args = ['root', 'handle', self.classid, 'htb']
        self._ensure_qdisc(args)

    def create_nat(self, floating_ip, fixed_ip):
        fixed_ip = '%s/32' % fixed_ip
        args = [
            'u32', 'match', 'ip', 'src', fixed_ip,
            'action', 'nat', 'egress', fixed_ip, floating_ip]
        self._manage_filter('add', args)


class BiDirectionNat(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def update_nats(nats):
        pass


class StatelessNat(BiDirectionNat):

    def __init__(self, interface):
        self.backends = IngressNat(interface), EgressNat(interface)

    def update_nats(self, nats):
        for backend in self.backends:
            backend.update_nats(nats)
