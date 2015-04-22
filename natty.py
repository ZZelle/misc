#!/usr/bin/env python
# Based on http://linux.programdevelop.com//2898840/

import subprocess
import sys

def ensure_qdisc(interface, spec):
    cmd = ['tc', 'qdisc', 'add', 'dev', interface]
    cmd.extend(spec)
    code = subprocess.call(cmd)
    return code in [0, 2]

def ensure_ingress_qdisc(interface):
    spec = 'ingress', 'handle', 'ffff'
    return ensure_qdisc(interface, spec)

def ensure_egress_qdisc(interface):
    spec = 'root', 'handle', '10:', 'htb'
    return ensure_qdisc(interface, spec)

def create_ingress_nat(interface, floating_ip, fixed_ip):
    ensure_ingress_qdisc(interface)

    floating_ip = '%s/32' % floating_ip
    cmd = [
        'tc','filter', 'add', 'dev', interface, 'parent', 'ffff:',
        'protocol', 'ip', 'prio', '10', 'u32',
        'match', 'ip', 'dst', floating_ip,
        'action', 'nat', 'ingress', floating_ip, fixed_ip
    ]
    code = subprocess.call(cmd)

def create_egress_nat(interface, floating_ip, fixed_ip):
    ensure_egress_qdisc(interface)

    fixed_ip = '%s/32' % fixed_ip
    cmd = [
        'tc','filter', 'add', 'dev', interface, 'parent', '10:',
        'protocol', 'ip', 'prio', '10', 'u32',
        'match', 'ip','src', fixed_ip,
        'action', 'nat', 'egress', fixed_ip, floating_ip
    ]
    code = subprocess.call(cmd)

def create_nat(interface, floating_ip, fixed_ip):
    create_ingress_nat(interface, floating_ip, fixed_ip)
    create_egress_nat(interface, floating_ip, fixed_ip)

def clean_nat(interface):
    cmd = ['tc', 'qdisc', 'del', 'dev', interface, 'parent', 'ffff:']
    code = subprocess.call(cmd)
    cmd = ['tc', 'qdisc', 'del', 'dev', interface, 'root', 'handle', '10:']
    code = subprocess.call(cmd)

def _list_nat(interface, parent):
    cmd = ['tc', 'filter', 'show', 'dev', interface, 'parent', parent]
    return subprocess.check_output(cmd)

def list_ingress_nat(interface):
    print _list_nat(interface, 'ffff:')

def list_egress_nat(interface):
    print _list_nat(interface, '10:')

def list_nat(interface):
    list_ingress_nat(interface)
    list_egress_nat(interface)


if __name__ == '__main__':
    method = sys.argv[1]
    args = sys.argv[2:]
    if method == 'create':
        create_nat(*args)
    elif method == 'delete':
        raise
    elif method == 'list':
        list_nat(*args)
    elif method == 'clean':
        clean_nat(*args)
    else:
        raise NotImplementedError

