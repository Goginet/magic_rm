#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

import os
import shutil

class MagicTrasher(object):

    def __init__(self, trash_path=None):
        self.trash_path = trash_path

    def move_to_trash(self, path, root_dir):
        if root_dir is None:
            # TODO: raise NoneRootExeption
            return

        if self.trash_path != None:
            def inc_path(path, index):
                new_path = path + "_({})".format(index)
                if os.path.exists(new_path):
                    return inc_path(path, index + 1)
                else:
                    return new_path

            relpath = os.path.relpath(path, start=root_dir)

            file_path = os.path.join(self.trash_path, relpath)

            dir_path = os.path.dirname(file_path)

            if not os.path.exists(self.trash_path):
                os.makedirs(self.trash_path)

            if dir_path == self.trash_path:
                if os.path.exists(file_path):
                    file_path = inc_path(file_path, 1)
            else:
                if os.path.exists(dir_path):
                    dir_path = inc_path(dir_path, 1)

                os.makedirs(dir_path)

            shutil.copy(path, file_path)

        else:
            self.alert("Trash path not set")

    def alert(self, message):
        print message
