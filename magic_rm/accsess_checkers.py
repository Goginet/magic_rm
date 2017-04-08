#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

from magic_rm.logger import Logger
from magic_rm.errors import RemoveFromDirError, CopyError, GoInsideDirError

def check_access_remove(func):
    def wrapper(self, path):
        try:
            func(self, path)
        except IOError as err:
            self.alert(err.strerror, Logger.ERROR, RemoveFromDirError)

    return wrapper

def check_access_copy(func):
    def wrapper(self, src, dst):
        try:
            func(self, src, dst)
        except IOError as err:
            self.alert(err.strerror, Logger.ERROR, CopyError)

    return wrapper

def check_go_inside(func):
    def wrapper(self, path):
        try:
            func(self, path)
        except OSError as err:
            self.alert(err.strerror, Logger.ERROR, GoInsideDirError)

    return wrapper
