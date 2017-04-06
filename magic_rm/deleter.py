#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

import stat
import os
import sys

from magic_rm.errors import *
from magic_rm.logger import Logger


class MagicDeleter(object):

    def __init__(self,
                 force=False,
                 interactive=False,
                 recursive=False,
                 empty_dir=False,
                 trasher=None,
                 no_remove=False,
                 symlinks=False,
                 logger=None):
        self.force = force
        self.interactive = interactive
        self.recursive = recursive
        self.empty_dir = empty_dir
        self.is_remove = not no_remove
        self.trasher = trasher
        self.logger = logger
        self.symlinks = symlinks
        self.__used_symlinks = []

    def remove(self, path):
        if not os.path.exists(path):
            self.alert("Cannot remove '{}': No such file or directory".format(path),
                       Logger.ERROR, DeleterNotFoundError)
        else:
            if self.trasher != None:
                self.trasher.move_to_trash(path)

            self._remove(path)

    def remove_dir(self, path):
        def remove(path):
            if self.recursive | self.empty_dir:
                if len(os.listdir(path)) == 0:
                    self._remove_empty_dir(path)
                elif self.recursive:
                    self._remove_content(path)
                else:
                    self.alert("Cannot remove '{}': Directory not empty".format(path),
                               Logger.ERROR, DeleterNotEmptyError)
            else:
                self.alert("Cannot remove '{}': Is a directory".format(path),
                           Logger.ERROR, DeleterNotFileError)

        if os.access(path, os.W_OK):
            if self.ask("descend into directory '{}'?".format(path)):
                remove(path)
        elif self.ask("descend into write-protected directory '{}'?".format(path), warning=True):
            remove(path)

    def remove_file(self, path):
        def remove():
            if self.is_remove:
                self.__rmfile(path)

        if os.access(path, os.W_OK):
            if self.ask("remove regular file '{}'?".format(path)):
                remove()
        elif self.ask("remove write-protected regular file'{}'?".format(path), warning=True):
            remove()

    def _remove_not_link(self, path):
        if os.path.isdir(path):
            self.remove_dir(path)
        elif os.path.isfile(path):
            self.remove_file(path)

    def _go_to_link(self, path):
        inode = os.stat(path).st_ino
        realpath = os.readlink(path)

        if inode not in self.__used_symlinks:
            self.__used_symlinks.append(inode)
            self._remove_not_link(realpath)

    def _remove(self, path):
        if os.path.islink(path):
            if self.symlinks:
                self._go_to_link(path)

            self.__unlink(path)
        else:
            self._remove_not_link(path)

    def _remove_content(self, path):
        for el in os.listdir(path):
            try:
                self._remove(os.path.join(path, el))
            except OSError as err:
                self.alert(err.strerror, Logger.ERROR, DeleterRemoveError)

        if len(os.listdir(path)) == 0:
            self._remove_empty_dir(path)

    def _remove_empty_dir(self, path):
        try:
            def rmdir():
                if self.is_remove:
                    self.__rmdir(path)

            if os.access(path, os.W_OK):
                if self.ask("remove directory '{}'?".format(path)):
                    rmdir()
            elif self.ask("remove protected directory '{}'?".format(path), warning=True):
                rmdir()
        except OSError as err:
            self.alert(err.strerror, Logger.ERROR)

    def __unlink(self, path):
        self.alert("remove '{}' symlink".format(path), Logger.DEBUG)
        os.unlink(path)

    def __rmdir(self, path):
        self.alert("remove '{}' directory".format(path), Logger.DEBUG)
        os.rmdir(path)

    def __rmfile(self, path):
        self.alert("remove {} file".format(path), Logger.DEBUG)
        os.remove(path)

    def alert(self, message, message_type, error_type=None):
        if self.logger != None:
            self.logger.alert(message, message_type)

        if message_type == Logger.ERROR and error_type != None:
            if not self.force:
                raise error_type(message)

    def ask(self, question, default="yes", warning=False):
        if not self.force and (self.interactive or warning):
            valid = {"yes": True, "y": True, "ye": True,
                     "no": False, "n": False}
            if default is None:
                prompt = " [y/n] "
            elif default == "yes":
                prompt = " [Y/n] "
            elif default == "no":
                prompt = " [y/N] "
            else:
                raise ValueError("invalid default answer: '%s'" % default)

            while True:
                sys.stdout.write(question + prompt)
                choice = raw_input().lower()
                if default is not None and choice == '':
                    return valid[default]
                elif choice in valid:
                    return valid[choice]
                else:
                    sys.stdout.write("Please respond with 'yes' or 'no' "
                                     "(or 'y' or 'n').\n")
        else:
            return True
