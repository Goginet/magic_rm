#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.
import json
import os

import toml

from magic_rm.cmd.get_default_configs import *
from magic_rm.cmd.parse_args import parse_args
from magic_rm.deleter import MagicDeleter
from magic_rm.errors import Error
from magic_rm.logger import Logger
from magic_rm.trasher import MagicTrasher


def grouped_args(args, new_args, *groups):
    for group in groups:
        if new_args.get(group) is None:
            new_args.update({group: {}})

    for name, value in args.iteritems():
        dest = name.split(".", 2)
        if len(dest) > 1:
            if new_args.get(dest[0]) is None:
                new_args.update({dest[0]: {}})
            new_args.get(dest[0]).update({dest[1]: value})
        else:
            new_args.update({dest[0]: value})
    return new_args

def load_toml_config(path):
    config_args = {}

    if not os.path.exists(path):
        with open(path, "w") as config_file:
            config_file.write(get_default_config_toml())

    with open(path) as config_file:
        config_args = toml.load(config_file)

    return config_args

def load_json_config(path):
    config_args = {}

    if not os.path.exists(path):
        with open(path, "w") as config_file:
            config_file.write(get_default_config_json())

    with open(path) as config_file:
        config_args = json.load(config_file)

    return config_args

def print_trash_list(trasher):
    meta = trasher.list_trash()
    template = "|{:^30}|{:^30}|{:^30}|"
    print template.format('item', 'time', "retention")
    print "|{:-^30}|{:-^30}|{:-^30}|".format('', '', '')
    for name, el in meta.iteritems():
        print template.format(name, el['time'].strftime("%y-%m-%d %H:%M:%S"), el['retention'])

def get_args():
    args, groups = parse_args()

    if args.get('config_json') != None:
        config_args = load_json_config(args.get('config_json'))
    elif args.get('config_toml') != None:
        config_args = load_toml_config(args.get('config_toml'))

    return grouped_args(args, config_args, *groups)

def main():
    args = get_args()

    def create_trasher(logger):
        args['trash'].update(args['restore'])
        return MagicTrasher(logger=logger, **args['trash'])

    def create_deleter(trasher, logger):
        return MagicDeleter(trasher=trasher, logger=logger, **args['remove'])

    def create_logger():
        return Logger(**args['logger'])

    def run():
        logger = create_logger()
        if args['command'] == 'remove':
            trasher = create_trasher(logger)
            deleter = create_deleter(trasher, logger)
            for path in args['PATH']:
                deleter.remove(path)
        if args['command'] == 'trash-list':
            trasher = create_trasher(logger)
            print_trash_list(trasher)
        if args['command'] == 'restore':
            trasher = create_trasher(logger)
            for path in args['PATH']:
                trasher.restore(path)
        if args['command'] == 'flush':
            trasher = create_trasher(logger)
            trasher.flush()
        if args['command'] == 'simple-config':
            if args['json']:
                print get_default_config_json()
            else:
                print get_default_config_toml()

    try:
        run()
    except Error as err:
        exit(err.code)

if __name__ == '__main__':
    main()
