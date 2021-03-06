#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

import re
import stat
import os
import sys

from magic_rm.accsess_checkers import check_go_inside
from magic_rm.errors import *
from magic_rm.logger import Logger


class MagicWalker(object):

    """Object for for walk to the directories tree.
    Keyword Arguments:
        - force -- if force is true, ignore all errors
        - recursive -- remove recursive
        - symlinks -- go to symlinks
        - regexp -- regular expression for remove
        - logger -- logger object
        - link_handler -- func which will be called when walker find link
        - file_handler -- func which will be called when walker find file
        - after_go_to_dir_handler -- func which will be called when walker go out from the directory
        - before_go_to_dir_handler -- func which will be called before go to directory
    """

    def __init__(self,
                 force=False,
                 recursive=True,
                 symlinks=False,
                 regexp=None,
                 logger=None,
                 link_handler=None,
                 file_handler=None,
                 after_go_to_dir_handler=None,
                 before_go_to_dir_handler=None):

        self.regexp = regexp
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
        self._walk(path)

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

    @check_go_inside
    def _go_to_dir(self, path):
        def remove(path):
            if self.recursive:
                self._call_content(path)

            self.__call_after_go_to_dir(path)

        remove(path)

    def __check_regexp(self, regexp, path):
        if regexp != None:
            rez = re.search(regexp, path)

            if rez != None:
                if rez.group(0) == path:
                    return True

            self.alert(
                "File not deleted '{}': Does not match the pattern.".format(path),
                Logger.DEBUG
            )

            return False
        else:
            return True

    def _call_content(self, path):
        content = os.listdir(path)
        self.__call_befor_go_to_dir(path)
        for el in content:
            self._walk(os.path.join(path, el))

    def __call_when_file(self, path):
        if self.file_handler != None:
            if self.__check_regexp(self.regexp, path):
                self.file_handler(path)

    def __call_befor_go_to_dir(self, path):
        if self.before_go_to_dir_handler != None:
            if self.__check_regexp(self.regexp, path):
                self.before_go_to_dir_handler(path)

    def __call_after_go_to_dir(self, path):
        if self.after_go_to_dir_handler != None:
            self.after_go_to_dir_handler(path)

    def __call_when_link(self, path):
        if self.link_handler != None:
            self.link_handler(path)

    def alert(self, message, message_type, error_type=None):
        if self.logger != None:
            self.logger.alert(message, message_type)

        if message_type == Logger.ERROR and error_type != None:
            if not self.force:
                raise error_type(message)
