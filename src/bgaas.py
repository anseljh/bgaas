#!/usr/bin/env python

# Copyright 2014 Ansel Halliburton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division

import argparse
import csvkit
import requests
import os
import logging

##############################################################################

log = logging.getLogger('bgaas')
log.setLevel(logging.DEBUG)
# add a console handler
# https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

##############################################################################

BGAAS_DIR = os.path.expanduser('~/.bgaas')
BGAAS_DATA_DIR = BGAAS_DIR + os.sep + 'data'
LISTS = ['csl', 'dpl', 'sdn', 'debar']
LIST_NAMES = {
    'csl': 'Consolidated Screening List',
    'dpl': 'Denied Persons List',
    'sdn': 'Specially Designated Nationals list',
    'debar': 'AECA debarment list'
}
RAW_SOURCES = {
    'csl': 'http://www.bis.doc.gov/export_consolidated_list/consolidated_party_list_final.csv',
    'dpl': 'http://www.bis.doc.gov/dpl/dpl.txt',
    'sdn': 'http://www.treasury.gov/ofac/downloads/sdn.csv', #TODO: other CSV files listed at http://www.treasury.gov/resource-center/sanctions/SDN-List/Pages/default.aspx
    'debar': None #TODO: Parse XLS or HTML version
    }

##############################################################################

def get_data_dir(args):
    if args.data_dir:
        log.debug("got data dir arg, setting to %s" % args.data_dir)
        dir_name = args.data_dir
    else:
        dir_name = BGAAS_DATA_DIR

    # check if exists; create if necessary
    if not os.path.exists(BGAAS_DATA_DIR):
        log.info("Creating directory: %s" % BGAAS_DATA_DIR)
        os.makedirs(BGAAS_DATA_DIR)
    return dir_name

def do_update(args):
    """Update arms control lists"""
    # if args.verbosity > 0:
    log.info("Verbosity: %d" % args.verbosity)
    log.info("Data directory: %s" % get_data_dir(args))
    log.info("Updating...")
    csl = update_list(args, 'csl')
    # if args.verbosity > 0:
    log.info("Done.")
    return True

def update_list(args, list_):
    # Check for 'all' as argument:
    if list_ == 'all':
        list_ = LISTS
    # Convert list_ to a single-element list if it's just a string:
    if type(list_) is str:
        list_ = [list_]
    if 'csl' in list_:
        output_fn = get_data_dir(args) + os.sep + 'csl'
        url = RAW_SOURCES['csl']
        log.debug("Fetching: %s" % url)
        r = requests.get(url)
        size = int(r.headers.get('content-length'))
        etag = r.headers.get('etag')
        content_type = r.headers.get('content-type')
        content = r.content
        log.debug("Received %.2f MiB" % (size / 1024 / 1024))
        assert content_type == 'text/plain', "content-type must be 'text/plain', but got '%s' instead." % content_type
        log.debug("Writing output for CSL to %s" % output_fn)
        output_f = open(output_fn, 'wb')
        output_f.write(content)
        output_f.close()
    elif 'dpl' in list_:
        raise Warning("DPL not implemented")
    elif 'sdn' in list_:
        raise Warning("SDN not implemented")
    elif 'debar' in list_:
        raise Warning("Debarment list not implemented")
    else:
        raise ValueError("invalid list name: %s" % list_)
        return False

def do_query(args):
    log.debug("Recieved query with: %s" % args.Q)

def do_map(args):
    log.debug("Recieved map query with: %s" % args.Q)

##############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='bgaas',
        description='Bad Guys As A Service: Slice and dice arms control data for fun and profit.'
        )
    subparsers = parser.add_subparsers(title='subcommands')
    parser.add_argument("-v", "--verbosity", action="count", help="increase output verbosity", default=0)
    parser.add_argument("-l", "--list", help="use specified list", choices=['csl', 'dpl', 'sdn', 'debar'])
    parser.add_argument("-d", "--data-dir", help="set data directory (defaults to %s)" % BGAAS_DATA_DIR, default=BGAAS_DATA_DIR)
    update_parser = subparsers.add_parser('update', help='Update list data')
    update_parser.set_defaults(func=do_update)
    query_parser = subparsers.add_parser('query', help='Query lists', usage='bgaas query Q')
    query_parser.add_argument('Q', help='The query term')
    query_parser.set_defaults(func=do_query)
    map_parser = subparsers.add_parser('map', help='Query and make a map', usage='bgaas map Q')
    map_parser.add_argument('Q', help='The query term')
    map_parser.set_defaults(func=do_map)

    args = parser.parse_args()
    args.func(args)
