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

class NotFoundError(Error):
    code = 200

class NotExistsError(Error):
    code = 201

class NotIndexedError(Error):
    code = 203

class NotEmptyError(Error):
    code = 204

class RemoveFromDirError(Error):
    code = 205

class CopyError(Error):
    code = 206

class GoInsideDirError(Error):
    code = 207

class CopyTrashIntoTrash(Error):
    code = 208
