#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.
import argparse

import isodate

import magic_rm.trasher
from magic_rm.logger import Logger


def parse_args():
    parser = argparse.ArgumentParser(description='****Magic remove tool****')

    subparser = parser.add_subparsers(dest='command', title='commands')

    remove_parser = subparser.add_parser('remove', formatter_class=argparse.RawTextHelpFormatter)
    restore_parser = subparser.add_parser('restore')
    subparser.add_parser('flush')
    subparser.add_parser('trash-list')
    subparser.add_parser('simple-config')


    remove_parser.add_argument('PATH', nargs='+', help='output version information and exit')
    restore_parser.add_argument('PATH', nargs='+', help='output version information and exit')


    parser.add_argument('--log-level', choices=Logger.LEVELS, dest='logger.log_level',
                        default=argparse.SUPPRESS, help='Level for logging to file')
    parser.add_argument('--verbose-level', choices=Logger.LEVELS, dest='logger.verbose_level',
                        default=argparse.SUPPRESS, help='Level for logging to stdout')
    parser.add_argument('--log-mode', choices=Logger.FORMATS, dest='logger.mode',
                        default=argparse.SUPPRESS, help='Formatter mode for log messages')
    parser.add_argument('--log-path', action='store', dest='logger.file_path',
                        default=argparse.SUPPRESS, help='Path to config file')
    parser.add_argument('--dry-run', choices=Logger.LEVELS, dest='logger.log_level',
                        default=argparse.SUPPRESS, help='Level for logging to file')


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

    parser.add_argument('--trash_path', action='store', dest='trash.trash_path',
                        default=argparse.SUPPRESS, help='Path to trash directory')


    remove_parser.add_argument('--regexp', action='store',
                               dest='remove.regexp', default=argparse.SUPPRESS,
                               help='Regexp template for removed files')
    remove_parser.add_argument('-l', '--symlinks', action='store_true',
                               dest='remove.symlinks', default=argparse.SUPPRESS,
                               help='Follow the symlinks')
    remove_parser.add_argument('--progress', action='store_true',
                               dest='general.progress', default=argparse.SUPPRESS,
                               help='Show progress for long operations')
    remove_parser.add_argument('-r', '--recursive', action='store_true', dest='remove.recursive',
                               default=argparse.SUPPRESS,
                               help='remove directories and their contents recursively')
    remove_parser.add_argument('-d', '--dir', action='store_true', dest='remove.dir',
                               default=argparse.SUPPRESS, help='remove empty directories')
    remove_parser.add_argument('--retention', action='store', dest='remove.retention',
                               type=isodate.parse_duration,
                               help=("File retention time in the trash\n"
                                     "formats:\n"
                                     "\tP1Y1M1D (1 year, 1 month, 1 day),\n"
                                     "\tPT1H1M1S (1 hour, 1 minute, 1 sec))\n"))


    restore_parser.add_argument('--progress', action='store_true',
                                dest='general.progress', default=argparse.SUPPRESS,
                                help='Show progress for long operations')
    restore_parser.add_argument('-f', '--force', action='store_true',
                                dest='general.force', default=argparse.SUPPRESS,
                                help='Ignore all errors')

    restore_mode_group = restore_parser.add_mutually_exclusive_group()
    restore_mode_group.add_argument('-r', '--replace', action='store_const',
                                    dest='restore.conflict_resolve', default=argparse.SUPPRESS,
                                    const=magic_rm.fs.REPLACE,
                                    help='restore when item already exists')
    restore_mode_group.add_argument('-s', '--skip', action='store_const',
                                    dest='restore.conflict_resolve', default=argparse.SUPPRESS,
                                    const=magic_rm.fs.SKIP,
                                    help='restore when item already exists')


    return vars(parser.parse_args()), ['general', 'remove', 'restore', 'trash', 'logger']
