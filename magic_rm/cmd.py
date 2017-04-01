#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.
import argparse
import toml
import os
import json
import isodate
from magic_rm.deleter import MagicDeleter
from magic_rm.trasher import MagicTrasher
from magic_rm.logger import Logger

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
            config_file.write(simple_config_toml())

    with open(path) as config_file:
        config_args = toml.load(config_file)

    return config_args

def load_json_config(path):
    config_args = {}

    if not os.path.exists(path):
        with open(path, "w") as config_file:
            config_file.write(simple_config_json())

    with open(path) as config_file:
        config_args = json.load(config_file)

    return config_args

def parse_args():
    parser = argparse.ArgumentParser(description='****Magic remove tool****')

    subparser = parser.add_subparsers(dest='command', title='commands')

    remove_parser = subparser.add_parser('remove', formatter_class=argparse.RawTextHelpFormatter)
    restore_parser = subparser.add_parser('restore')
    subparser.add_parser('flush')
    subparser.add_parser('trash-list')
    print_config_parser = subparser.add_parser('simple-config')

    remove_parser.add_argument('-f', '--force', action='store_true', dest='remove.force',
                               default=argparse.SUPPRESS,
                               help='ignore nonexistent files and arguments, never prompt')
    remove_parser.add_argument('-i', action='store_true', dest='remove.interactive',
                               default=argparse.SUPPRESS, help='prompt before every removal')
    remove_parser.add_argument('-r', '-R', action='store_true', dest='remove.recursive',
                               default=argparse.SUPPRESS,
                               help='remove directories and their contents recursively')
    remove_parser.add_argument('-d', '--dir', action='store_true', dest='remove.empty_dir',
                               default=argparse.SUPPRESS, help='remove empty directories')
    remove_parser.add_argument('--no-trash', action='store_true', dest='trash.no_trash',
                               default=argparse.SUPPRESS, help='Don\'t save files in trash')
    remove_parser.add_argument('--no-remove', action='store_true', dest='remove.no_remove',
                               default=argparse.SUPPRESS, help='Don\'t remove files')
    remove_parser.add_argument('--retention', action='store', dest='restore.retention',
                               type=isodate.parse_duration,
                               help=("File retention time in the trash\n"
                                     "formats:\n"
                                     "\tP1Y1M1D (1 year, 1 month, 1 day),\n"
                                     "\tPT1H1M1S (1 hour, 1 minute, 1 sec))\n"))

    restore_parser.add_argument('-f', '--force', action='store_true', dest='restore.force',
                                default=argparse.SUPPRESS, help='restore when item already exists')

    parser.add_argument('--trash_path', action='store', dest='trash.path',
                        default=argparse.SUPPRESS, help='Path to trash directory')
    parser.add_argument('--log-level', choices=Logger.LEVELS, dest='logger.log_level',
                        default=argparse.SUPPRESS, help='Level for logging to file')
    parser.add_argument('--verbose-level', choices=Logger.LEVELS, dest='logger.verbose_level',
                        default=argparse.SUPPRESS, help='Level for logging to stdout')
    parser.add_argument('--log-mode', choices=Logger.FORMATS, dest='logger.mode',
                        default=argparse.SUPPRESS, help='Formatter mode for log messages')
    parser.add_argument('--log-path', action='store', dest='logger.file_path',
                        default=argparse.SUPPRESS, help='Path to config file')


    print_config_group = parser.add_mutually_exclusive_group()
    print_config_group.add_argument('--toml', action='store_true', dest='toml',
                                    default="magic_rm.conf", help='Print toml config')
    print_config_group.add_argument('--json', action='store_true', dest='json',
                                    default="magic_rm.conf", help='Print json config')

    config_group = parser.add_mutually_exclusive_group()
    config_group.add_argument('--config', action='store', dest='config_toml',
                              default="magic_rm.conf", help='Path to config file (TOML format)')
    config_group.add_argument('--config-json', action='store', dest='config_json',
                              help='Path to config file (JSON format)')

    remove_parser.add_argument('PATH', nargs='+', help='output version information and exit')
    restore_parser.add_argument('PATH', nargs='+', help='output version information and exit')

    args = vars(parser.parse_args())

    if args.get('config_json') != None:
        config_args = load_json_config(args.get('config_json'))
    elif args.get('config_toml') != None:
        config_args = load_toml_config(args.get('config_toml'))

    return grouped_args(args, config_args, 'remove', 'restore', 'trash', 'logger')

def print_trash_list(trasher):
    meta = trasher.list_trash()
    template = "|{:^30}|{:^30}|{:^30}|"
    print template.format('item', 'time', "retention")
    print "|{:-^30}|{:-^30}|{:-^30}|".format('', '', '')
    for name, el in meta.iteritems():
        print template.format(name, el['time'].strftime("%y-%m-%d %H:%M:%S"), el['retention'])

def main():
    args = parse_args()

    def create_trasher(logger):
        args['trash'].update(args['restore'])
        return MagicTrasher(logger=logger, **args['trash'])

    def create_deleter(trasher, logger):
        return MagicDeleter(trasher=trasher, logger=logger, **args['remove'])

    def create_logger():
        return Logger(**args['logger'])

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
            print simple_config_json()
        else:
            print simple_config_toml()

def simple_config_toml():
    return '''
[remove]
    # force = true
    # interactive = true
    # recursive = true
    # empty_dir = true
    # no_remove = true

    ### File retention time in the trash
    ### formats: P1Y1M1D (1 year, 1 month, 1 day), PT1H1M1S (1 hour, 1 minute, 1 sec)
    # retention = P1D

[restore]
    # force = true

[logger]
    log_level = "ERROR"
    verbose_level = "WARNING"
    mode = "JSON"
    file_path = "magic_rm.log"

[trash]
    # no_trash = true
    path = "trash"
'''

def simple_config_json():
    return '''
{
    "remove": {
        // "force": true,
        // "interactive": true,
        // "recursive": true,
        // "empty_dir": true,
        // "no_remove": true,
        // "retention": "P1D"
    },
    "restore": {
        // "force": true
    },
    "logger": {
        "log_level": "ERROR",
        "verbose_level": "WARNING",
        "mode": "JSON",
        "file_path": "magic_rm.log"
    },
    "trash": {
        // "no_trash": true,
        "path": "trash",
    }
}
'''

if __name__ == '__main__':
    main()