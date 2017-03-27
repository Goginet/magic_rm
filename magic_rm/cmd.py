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

    remove_parser.add_argument('-f', '--force', action='store_true', dest='force',
                               help='ignore nonexistent files and arguments, never prompt')
    remove_parser.add_argument('-i', action='store_true', dest='interactive',
                               help='prompt before every removal')
    remove_parser.add_argument('-r', '-R', action='store_true', dest='recursive',
                               help='remove directories and their contents recursively')
    remove_parser.add_argument('-d', '--dir', action='store_true', dest='emptyDir',
                               help='remove empty directories')

    remove_parser.add_argument('--no-trash', action='store_true', dest='no_trash',
                               help='Don\'t save files in trash')
    remove_parser.add_argument('--no-remove', action='store_true', dest='no_remove',
                               help='Don\'t remove files')
    remove_parser.add_argument('--trash_path', action='store', dest='trash_path',
                               default="/home/goginet/trasher", help='Path to trash directory')

    parser.add_argument('PATH', nargs='+', help='output version information and exit')

    return parser.parse_args()

def main():
    args = parse_args()

    trasher = MagicTrasher(trash_path=args.trash_path)
    deleter = MagicDeleter(force=args.force,
                           interactive=args.interactive,
                           recursive=args.recursive,
                           empty_dir=args.emptyDir,
                           trasher=trasher,
                           no_remove=args.no_remove)

    if args.command == 'remove':
        for path in args.PATH:
            deleter.remove(path)

if __name__ == '__main__':
    main()
