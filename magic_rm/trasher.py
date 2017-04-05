#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

import os
import shutil
import pickle
import datetime
from magic_rm.logger import Logger
from magic_rm.errors import *

def meta_update(func):
    def wrapper(self, *args):
        trash_items = {}

        rez = {}

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

    def __init__(self, logger=None, path="magic_trash", force=False, retention=None):
        self.path = path
        self.force = force
        self.retention = retention
        self.meta_file_path = os.path.join(path, "meta.db")
        self.logger = logger

    def move_to_trash(self, path):
        if os.path.exists(path):
            self.flush()

            path = os.path.abspath(path)

            path_in_trash = os.path.join(self.path, os.path.basename(path))

            self._move_to_trash(path, path_in_trash)
        else:
            self.__alert("Cannot move to trash '{}': No such file or directory".format(path),
                         Logger.ERROR, TrasherNotFoundError)

    def restore(self, item_name):
        item = self._meta_list().get(item_name)

        if item is None:
            self.__alert("Item: \'{}\' does not exists in trash.".format(item_name),
                         Logger.ERROR, TrasherNotExistsError)
            return

        if not os.path.exists(item["real_path"]) or self.force:
            self._restore_item(item_name, item)
        else:
            self.__alert("Can't restore item, item already exists",
                         Logger.ERROR, TrasherRestoreConflict)

    def flush(self):
        self.flush_by_retention_time()

    def flush_by_retention_time(self):
        items = self._meta_list()

        for name, value in items.iteritems():
            if value.get("retention") != None:
                end_time = value.get("time") + value.get("retention")
                if datetime.datetime.now() > end_time:
                    self._remove_item(name)

    def list_trash(self):
        return self._meta_list()

    def _move_to_trash(self, path, path_in_trash):
        def inc_path(path, index):
            new_path = "{}_({})".format(path, index)
            if os.path.exists(new_path):
                return inc_path(path, index + 1)
            else:
                return new_path

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if os.path.exists(path_in_trash):
            path_in_trash = inc_path(path_in_trash, 1)

        self.__copy_dir_or_file(path, path_in_trash)

        self._meta_add(path_in_trash, path)


    def _restore_item(self, item_name, item):
        self.__remove_dir_or_file(item.get("real_path"))

        dest = os.path.dirname(item.get("real_path"))
        if not os.path.exists(dest):
            os.makedirs(dest)

        path_in_trash = os.path.join(self.path, item_name)
        self.__copy_dir_or_file(path_in_trash, item.get("real_path"))
        self._remove_item(item_name)

    def _remove_item(self, name):
        path_in_trash = os.path.join(self.path, name)
        self.__remove_dir_or_file(path_in_trash)
        self._meta_remove(name)

    @meta_update
    def _meta_add(self, path_in_trash, path, trash_items=None):
        trash_items.update(
            {
                os.path.basename(path_in_trash): {
                    "real_path": path,
                    "time": datetime.datetime.now(),
                    "retention": self.retention
                }
            }
        )

    @meta_update
    def _meta_remove(self, item, trash_items=None):
        trash_items.pop(item)

    @meta_update
    def _meta_list(self, trash_items=None):
        return trash_items

    def __remove_dir_or_file(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    def __copy_dir_or_file(self, src, dest):
        if os.path.exists(src):
            if os.path.isdir(src):
                shutil.copytree(src, dest, symlinks=True)
            else:
                shutil.copy(src, dest)
        else:
            self.logger.alert("Can't found '{}' item in trash. It's lost.",
                              Logger.ERROR, TrasherNotIndexedError)

    def __alert(self, message, message_type, error_type=None):
        if self.logger != None:
            self.logger.alert(message, message_type)

        if message_type == Logger.ERROR and error_type != None:
            if not self.force:
                raise error_type(message)
