#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.
import argparse
from magic_rm.deleter import MagicDeleter

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

    parser.add_argument('PATH', nargs='+', help='output version information and exit')

    return parser.parse_args()

def main():
    args = vars(parse_args())

    deleter = MagicDeleter()

    for name, value in args.iteritems():
        if hasattr(deleter, name):
            setattr(deleter, name, value)

    if args['command'] == 'remove':
        for path in args['PATH']:
            deleter.remove(path)

if __name__ == '__main__':
    main()
