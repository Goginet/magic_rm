#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.
import json
import os

import toml
import sys

from magic_rm.cmd.parse_args import *
from magic_rm.cmd.get_default_configs import *
from magic_rm.cmd.parse_args import parse_args
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

def get_args(mode):
    args, groups = parse_args(mode)

    if args.get('config_json') != None:
        config_args = load_json_config(args.get('config_json'))
    elif args.get('config_toml') != None:
        config_args = load_toml_config(args.get('config_toml'))

    return grouped_args(args, config_args, *groups)

def main(mode=REMOVE):
    args = get_args(mode)

    def create_trasher(logger):
        kwargs = {}
        kwargs.update(args['trash'])
        kwargs.update(args['remove'])
        kwargs.update(args['restore'])
        kwargs.update(args['general'])
        return MagicTrasher(logger=logger, **kwargs)

    def create_logger():
        kwargs = {}
        kwargs.update(args['logger'])
        return Logger(**args['logger'])

    def run():
        logger = create_logger()
        if mode == REMOVE:
            trasher = create_trasher(logger)
            for path in args['PATH']:
                trasher.remove(path)
        if mode == TRASH_LIST:
            trasher = create_trasher(logger)
            print_trash_list(trasher)
        if mode == RESTORE:
            trasher = create_trasher(logger)
            for name in args['NAME']:
                trasher.restore(name)
        if mode == FLUSH:
            trasher = create_trasher(logger)
            trasher.flush()
        if mode == GET_DEFAULT_CONFIG:
            if args['json']:
                print get_default_config_json()
            else:
                print get_default_config_toml()

    try:
        if args['logger'].get('verbose_level') == Logger.SILENT:
            sys.stdout = open(os.devnull, "w")

        run()
    except Error as err:
        exit(err.code)

def remove():
    main(REMOVE)

def restore():
    main(RESTORE)

def trash_list():
    main(TRASH_LIST)

def flush():
    main(FLUSH)

def get_default_config():
    main(GET_DEFAULT_CONFIG)

if __name__ == '__main__':
    main()
