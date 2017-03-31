#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.
import argparse
import toml
import json
import isodate
from magic_rm.deleter import MagicDeleter
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
    with open(path) as config_file:
        config_args = toml.load(config_file)
        return config_args

def load_json_config(path):
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

    remove_parser.add_argument('-f', '--force', action='store_true', dest='remove.force',
                               help='ignore nonexistent files and arguments, never prompt')
    remove_parser.add_argument('-i', action='store_true', dest='remove.interactive',
                               help='prompt before every removal')
    remove_parser.add_argument('-r', '-R', action='store_true', dest='remove.recursive',
                               help='remove directories and their contents recursively')
    remove_parser.add_argument('-d', '--dir', action='store_true', dest='remove.empty_dir',
                               help='remove empty directories')
    remove_parser.add_argument('--no-trash', action='store_true', dest='trash.no_trash',
                               help='Don\'t save files in trash')
    remove_parser.add_argument('--no-remove', action='store_true', dest='remove.no_remove',
                               help='Don\'t remove files')
    remove_parser.add_argument('--retention', action='store', dest='restore.retention',
                               type=isodate.parse_duration,
                               help=("File retention time in the trash\n"
                                     "formats:\n"
                                     "\tP1Y1M1D (1 year, 1 month, 1 day),\n"
                                     "\tPT1H1M1S (1 hour, 1 minute, 1 sec))\n"))

    restore_parser.add_argument('-f', '--force', action='store_true', dest='restore.force',
                                help='restore when item already exists')

    parser.add_argument('--trash_path', action='store', dest='trash.path',
                        default="/home/goginet/trasher", help='Path to trash directory')

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

    return grouped_args(args, config_args, 'remove', 'restore', 'trash')

def print_trash_list(trasher):
    meta = trasher.list_trash()
    template = "|{:^30}|{:^30}|"
    print template.format('item', 'time')
    print "|{:-^30}|{:-^30}|".format('', '')
    for name, el in meta.iteritems():
        print template.format(name, el['time'].strftime("%y-%m-%d %H:%M:%S"))

def main():
    args = parse_args()

    def create_trasher():
        return MagicTrasher(trash_path=args['trash']['path'], **args['restore'])

    def create_deleter(trasher):
        return MagicDeleter(trasher=trasher, **args['remove'])

    if args['command'] == 'remove':
        trasher = create_trasher()
        deleter = create_deleter(trasher)
        for path in args['PATH']:
            deleter.remove(path)
    if args['command'] == 'trash-list':
        trasher = create_trasher()
        print_trash_list(trasher)
    if args['command'] == 'restore':
        trasher = create_trasher()
        for path in args['PATH']:
            trasher.restore(path)
    if args['command'] == 'flush':
        trasher = create_trasher()
        trasher.flush()

if __name__ == '__main__':
    main()
