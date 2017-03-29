#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.
import argparse
from magic_rm.deleter import MagicDeleter
from magic_rm.trasher import MagicTrasher

def parse_args():
    parser = argparse.ArgumentParser(description='****Magic remove tool****')

    subparser = parser.add_subparsers(dest='command', title='commands')

    remove_parser = subparser.add_parser('remove')
    restore_parser = subparser.add_parser('restore')
    trash_list_parser = subparser.add_parser('trash-list')

    remove_parser.add_argument('-f', '--force', action='store_true', dest='force',
                               help='ignore nonexistent files and arguments, never prompt')
    remove_parser.add_argument('-i', action='store_true', dest='interactive',
                               help='prompt before every removal')
    remove_parser.add_argument('-r', '-R', action='store_true', dest='recursive',
                               help='remove directories and their contents recursively')
    remove_parser.add_argument('-d', '--dir', action='store_true', dest='emptyDir',
                               help='remove empty directories')

    restore_parser.add_argument('-f', '--force', action='store_true', dest='force',
                                help='restore when item already exists')

    remove_parser.add_argument('--no-trash', action='store_true', dest='no_trash',
                               help='Don\'t save files in trash')
    remove_parser.add_argument('--no-remove', action='store_true', dest='no_remove',
                               help='Don\'t remove files')
    parser.add_argument('--trash_path', action='store', dest='trash_path',
                        default="/home/goginet/trasher", help='Path to trash directory')

    remove_parser.add_argument('PATH', nargs='+', help='output version information and exit')
    restore_parser.add_argument('PATH', nargs='+', help='output version information and exit')

    return parser.parse_args()

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
        return MagicTrasher(trash_path=args.trash_path,
                            force=getattr(args, "force", False))

    def create_deleter(trasher):
        return MagicDeleter(force=args.force,
                            interactive=args.interactive,
                            recursive=args.recursive,
                            empty_dir=args.emptyDir,
                            trasher=trasher,
                            no_remove=args.no_remove)

    if args.command == 'remove':
        trasher = create_trasher()
        deleter = create_deleter(trasher)
        for path in args.PATH:
            deleter.remove(path)
    if args.command == 'trash-list':
        trasher = create_trasher()
        print_trash_list(trasher)
    if args.command == 'restore':
        trasher = create_trasher()
        for path in args.PATH:
            trasher.restore(path)

if __name__ == '__main__':
    main()
