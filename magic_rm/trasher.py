#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

import os
import shutil
import pickle
import datetime

class MagicTrasher(object):

    def __init__(self, trash_path=None):
        self.trash_path = trash_path
        self.meta_file_path = os.path.join(trash_path, "meta.db")

    def update_meta_inf(self, path, real_path):
        trash_items = []
        if os.path.exists(self.meta_file_path):
            with open(self.meta_file_path, 'rb') as f:
                trash_items = pickle.load(f)

        trash_items.append({"path": path, "real_path": real_path, "time": datetime.datetime.now()})

        with open(self.meta_file_path, 'wb') as f:
            pickle.dump(trash_items, f)

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

            path = os.path.abspath(path)

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
            self.update_meta_inf(file_path, path)
        else:
            self.alert("Trash path not set")

    def alert(self, message):
        print message
