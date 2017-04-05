#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

class Error(Exception):
    code = 404
    def __init__(self, value):
        super(Error, self).__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)

class DeleterNotFoundError(Error):
    code = 100

class DeleterNotEmptyError(Error):
    code = 101

class DeleterNotFileError(Error):
    code = 102

class DeleterRemoveError(Error):
    code = 103

class TrasherNotFoundError(Error):
    code = 200

class TrasherNotExistsError(Error):
    code = 201

class TrasherRestoreConflict(Error):
    code = 202

class TrasherNotIndexedError(Error):
    code = 203
