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

    def update_meta_inf(self, path_in_trash, path):
        trash_items = []
        if os.path.exists(self.meta_file_path):
            with open(self.meta_file_path, 'rb') as f:
                trash_items = pickle.load(f)

        trash_items.append({"item": os.path.basename(path_in_trash),
                            "real_path": path, "time": datetime.datetime.now()})

        with open(self.meta_file_path, 'wb') as f:
            pickle.dump(trash_items, f)

    def move_to_trash(self, path):
        if self.trash_path != None:
            def inc_path(path, index):
                new_path = path + "_({})".format(index)
                if os.path.exists(new_path):
                    return inc_path(path, index + 1)
                else:
                    return new_path

            path = os.path.abspath(path)

            path_in_trash = os.path.join(self.trash_path, os.path.basename(path))

            if not os.path.exists(self.trash_path):
                os.makedirs(self.trash_path)

            if os.path.exists(path_in_trash):
                path_in_trash = inc_path(path_in_trash, 1)

            if os.path.isdir(path):
                shutil.copytree(path, path_in_trash, symlinks=True)
            else:
                shutil.copy(path, path_in_trash)

            self.update_meta_inf(path_in_trash, path)
        else:
            self.alert("Trash path not set")

    def alert(self, message):
        print message
