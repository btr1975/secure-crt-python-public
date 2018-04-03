import modules as mod
import itertools
import os
import sys
from ConfigParser import ConfigParser
import re
import urllib2
import json
from HTMLParser import HTMLParser
import webbrowser


screen_data = """
This product contains cryptographic features and is subject to United
States and local country laws test governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local loop laws, return this product immediately.
"""

screen_data_2 = """
This product contains cryptographic features and is subject to United
States and local country laws lip2 governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. moop By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.
"""

data = dict()

data['init'] = 'test-init.txt'
data['end'] = 'test-end.txt'
data['eigrp-pre'] = '{}-eigrp-pre.txt'
data['eigrp-post'] = '{}-eigrp-post.txt'
data['bgp-pre'] = '{}-bgp-pre.txt'
data['bgp-post'] = '{}-bgp-post.txt'
data['ospf-pre'] = '{}-ospf-pre.txt'
data['ospf-post'] = '{}-ospf-post.txt'
data['pim-pre'] = '{}-pim-pre.txt'
data['pim-post'] = '{}-pim-post.txt'
data['general-pre'] = '{}-general-pre.txt'
data['general-post'] = '{}-general-post.txt'
data['html'] = '{}-diff.html'
data['xls'] = '{}.xlsx'


def get_available_paired_files():

    dict_of_file_names = {
        'eigrp': {},
        'bgp': {},
        'pim': {},
        'ospf': {},
        'general': {},
        'config': {},
    }

    for key in data.keys():
        if 'eigrp' in key and 'pre' in key:
            dict_of_file_names['eigrp'].update({'pre': data.get(key)})

        elif 'eigrp' in key and 'post' in key:
            dict_of_file_names['eigrp'].update({'post': data.get(key)})

        elif 'bgp' in key and 'pre' in key:
            dict_of_file_names['bgp'].update({'pre': data.get(key)})

        elif 'bgp' in key and 'post' in key:
            dict_of_file_names['bgp'].update({'post': data.get(key)})

        elif 'pim' in key and 'pre' in key:
            dict_of_file_names['pim'].update({'pre': data.get(key)})

        elif 'pim' in key and 'post' in key:
            dict_of_file_names['pim'].update({'post': data.get(key)})

        elif 'ospf' in key and 'pre' in key:
            dict_of_file_names['ospf'].update({'pre': data.get(key)})

        elif 'ospf' in key and 'post' in key:
            dict_of_file_names['ospf'].update({'post': data.get(key)})

        elif 'general' in key and 'pre' in key:
            dict_of_file_names['general'].update({'pre': data.get(key)})

        elif 'general' in key and 'post' in key:
            dict_of_file_names['general'].update({'post': data.get(key)})

        elif 'init' in key:
            dict_of_file_names['config'].update({'pre': data.get(key)})

        elif 'end' in key:
            dict_of_file_names['config'].update({'post': data.get(key)})

    for pair in dict_of_file_names.keys():
        if not mod.verify_file_exists(dict_of_file_names.get(pair).get('pre'), '.') \
                or not mod.verify_file_exists(dict_of_file_names.get(pair).get('post'), '.'):
            dict_of_file_names.pop(pair)

    return dict_of_file_names


for key in get_available_paired_files().keys():
    print(key)