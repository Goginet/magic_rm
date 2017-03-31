#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

import os
import shutil
import pickle
import datetime

def meta_update(func):
    def wrapper(self, *args):
        trash_items = {}

        rez = {} # This is bad (

        if os.path.exists(self.path):
            if os.path.exists(self.meta_file_path):
                with open(self.meta_file_path, 'rb') as f:
                    trash_items = pickle.load(f)

            rez = func(self, *args, trash_items=trash_items)

            with open(self.meta_file_path, 'wb') as f:
                pickle.dump(trash_items, f)

        return rez

    return wrapper

class MagicTrasher(object):

    def __init__(self, path="magic_trash", force=False, retention=None):
        self.path = path
        self.force = force
        self.retention = retention
        self.meta_file_path = os.path.join(path, "meta.db")

    @meta_update
    def meta_add(self, path_in_trash, path, trash_items=None):
        trash_items.update({os.path.basename(path_in_trash): {"real_path": path,
                                                              "time": datetime.datetime.now(),
                                                              "retention": self.retention}})

    @meta_update
    def meta_remove(self, item, trash_items=None):
        trash_items.pop(item)

    @meta_update
    def meta_get(self, item, trash_items=None):
        return trash_items.get(item)

    @meta_update
    def meta_list(self, trash_items=None):
        return trash_items

    def flush(self):
        self.flush_by_retention_time()

    def flush_by_retention_time(self):
        items = self.meta_list()

        for name, value in items.iteritems():
            if value.get("retention") != None:
                end_time = value.get("time") + value.get("retention")
                if datetime.datetime.now() > end_time:
                    path_in_trash = os.path.join(self.path, name)
                    if os.path.isdir(path_in_trash):
                        shutil.rmtree(path_in_trash)
                    else:
                        os.remove(path_in_trash)
                    self.meta_remove(name)

    def move_to_trash(self, path):
        def inc_path(path, index):
            new_path = path + "_({})".format(index)
            if os.path.exists(new_path):
                return inc_path(path, index + 1)
            else:
                return new_path

        path = os.path.abspath(path)

        path_in_trash = os.path.join(self.path, os.path.basename(path))

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if os.path.exists(path_in_trash):
            path_in_trash = inc_path(path_in_trash, 1)

        if os.path.isdir(path):
            shutil.copytree(path, path_in_trash, symlinks=True)
        else:
            shutil.copy(path, path_in_trash)

        self.meta_add(path_in_trash, path)

    def list_trash(self):
        return self.meta_list()

    def restore(self, item_name):
        if self.path != None:
            def restore(path_in_trash, real_path):
                shutil.move(path_in_trash, real_path)
                self.meta_remove(item_name)

            item = self.meta_get(item_name)

            if item is None:
                self.alert("Item: \'{}\' does not exists in trash.".format(item_name))
                return

            path_in_trash = os.path.join(self.path, item_name)

            real_path = item.get("real_path")

            dest = os.path.dirname(real_path)

            if os.path.exists(real_path):
                if self.force:
                    if os.path.isdir(real_path):
                        shutil.rmtree(real_path)
                    else:
                        os.remove(real_path)
                    restore(path_in_trash, real_path)
                else:
                    self.alert("File exists")
            else:
                if not os.path.exists(dest):
                    os.makedirs(dest)
                restore(path_in_trash, real_path)
        else:
            self.alert("Trash path not set")

    def alert(self, message):
        print message
