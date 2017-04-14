#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

from magic_rm.logger import Logger
from magic_rm.errors import RemoveFromDirError, CopyError, GoInsideDirError, \
WorkWithFileError

def check_access_file(func):
    def wrapper(self, *args):
        try:
            rez = func(self, *args)
            return rez
        except IOError as err:
            self.alert(err.strerror, Logger.ERROR, WorkWithFileError)

    return wrapper

def check_access_remove(func):
    def wrapper(self, path):
        try:
            rez = func(self, path)
            return rez
        except IOError as err:
            self.alert(err.strerror, Logger.ERROR, RemoveFromDirError)

    return wrapper

def check_access_copy(func):
    def wrapper(self, src, dst):
        try:
            rez = func(self, src, dst)
            return rez
        except IOError as err:
            self.alert(err.strerror, Logger.ERROR, CopyError)

    return wrapper

def check_go_inside(func):
    def wrapper(self, path):
        try:
            rez = func(self, path)
            return rez
        except OSError as err:
            self.alert(err.strerror, Logger.ERROR, GoInsideDirError)

    return wrapper
