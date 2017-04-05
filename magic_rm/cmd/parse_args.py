#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.
import argparse

import isodate

from magic_rm.logger import Logger


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

    return vars(parser.parse_args()), ['remove', 'restore', 'trash', 'logger']
