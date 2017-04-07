#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

import stat
import os
import sys

from magic_rm.errors import *
from magic_rm.logger import Logger


class MagicWalker(object):

    def __init__(self,
                 force=False,
                 recursive=True,
                 symlinks=False,
                 logger=None,
                 link_handler=None,
                 file_handler=None,
                 after_go_to_dir_handler=None,
                 before_go_to_dir_handler=None):

        self.symlinks = symlinks
        self.recursive = recursive
        self.force = force
        self.logger = logger
        self.file_handler = file_handler
        self.link_handler = link_handler
        self.after_go_to_dir_handler = after_go_to_dir_handler
        self.before_go_to_dir_handler = before_go_to_dir_handler
        self.__used_symlinks = []

    def walk(self, path):
        if os.path.exists(path):
            self._walk(path)
        else:
            self.__alert("Cannot find '{}': No such file or directory".format(path),
                         Logger.ERROR, DeleterNotFoundError)

        self.__used_symlinks = []


    def _walk(self, path):
        if os.path.islink(path):
            if self.symlinks:
                if os.path.exists(path):    # check for broken symlinks
                    self._go_to_link(path)
                else:
                    self.__call_when_link(path)
            else:
                self.__call_when_link(path)
        else:
            self._go_to_not_link(path)

    def _go_to_link(self, path):
        inode = os.stat(path).st_ino

        if inode not in self.__used_symlinks:
            self.__used_symlinks.append(inode)

            self._go_to_not_link(path)

            self.__call_when_link(path)

    def _go_to_not_link(self, path):
        if os.path.isdir(path):
            self._go_to_dir(path)
        elif os.path.isfile(path):
            self.__call_when_file(path)

    def _go_to_dir(self, path):
        def remove(path):
            self.__call_befor_go_to_dir(path)
            if self.recursive:
                self._call_content(path)

            self.__call_after_go_to_dir(path)

        remove(path)

    def _call_content(self, path):
        for el in os.listdir(path):
            self._walk(os.path.join(path, el))

    def __call_when_file(self, path):
        if self.file_handler != None:
            self.file_handler(path)

    def __call_befor_go_to_dir(self, path):
        if self.before_go_to_dir_handler != None:
            self.before_go_to_dir_handler(path)

    def __call_after_go_to_dir(self, path):
        if self.after_go_to_dir_handler != None:
            self.after_go_to_dir_handler(path)

    def __call_when_link(self, path):
        if self.link_handler != None:
            self.link_handler(path)

    def __alert(self, message, message_type, error_type=None):
        if self.logger != None:
            self.logger.alert(message, message_type)

        if message_type == Logger.ERROR and error_type != None:
            if not self.force:
                raise error_type(message)
