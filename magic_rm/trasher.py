#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

import datetime
import os
import pickle

from magic_rm.accsess_checkers import check_go_inside
from magic_rm.fs import MagicFs, SKIP
from magic_rm.errors import NotFoundError, NotExistsError, NotIndexedError, NotEmptyError
from magic_rm.logger import Logger


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

    """Object for for work with trash dir.
    Keyword Arguments:
        - conflict_resolve -- mode for resolved conflicts (SKIP|MERGE)
        - recursive -- remove recursive
        - empty_dir -- remove empty dir
        - symlinks -- go to symlinks
        - logger -- logger object
        - path -- path to the trash dir
        - regexp -- regular expression for remove
        - force -- if force is true, ignore all errors
        - progress -- show progress bar for long operations
        - retention -- Time of file store in trash
    """

    def __init__(self,
                 conflict_resolve=SKIP,
                 recursive=False,
                 empty_dir=True,
                 symlinks=False,
                 logger=None,
                 path="magic_trash",
                 regexp=None,
                 force=False,
                 progress=False,
                 retention=None):

        self.conflict_resolve = conflict_resolve
        self.path = path
        self.regexp = regexp
        self.progress = progress
        self.retention = retention
        self.meta_file_path = os.path.join(path, "meta.db")
        self.logger = logger
        self.force = force
        self.recursive = recursive
        self.empty_dir = empty_dir

        self.fs = MagicFs(
            conflict=conflict_resolve,
            force=force,
            regexp=regexp,
            progress=progress,
            symlinks=symlinks,
            logger=logger,
        )

    """ Move file to trash """
    def remove(self, path):

        self._preremove(path)

        self.flush()

        path = os.path.abspath(path)

        path_in_trash = os.path.join(self.path, os.path.basename(path))

        self._move_to_trash(path, path_in_trash)

    """ Restore item from trash """
    def restore(self, item_name):
        self._prerestore(item_name)

        item = self._meta_list().get(item_name)

        if item is None:
            self.alert(
                "Item: \'{}\' does not exists in trash.".format(item_name),
                Logger.ERROR,
                NotExistsError
            )
            return

        self._restore_item(item_name, item)

    """ Remove old items """
    def flush(self):
        self.flush_by_retention_time()

    """ Remove old by retention time """
    def flush_by_retention_time(self):
        items = self._meta_list()

        for name, value in items.iteritems():
            if value.get("retention") != None:
                end_time = value.get("time") + value.get("retention")
                if datetime.datetime.now() > end_time:
                    self._remove_item(name)

    """ Get trash items """
    def list_trash(self):
        return self._meta_list()

    def _prerestore(self, item_name):
        self.fs.regexp = None

    @check_go_inside
    def _preremove(self, path):
        if not os.path.exists(path):
            self.alert(
                "Cannot move to trash '{}': No such file or directory".format(path),
                Logger.ERROR,
                NotFoundError
            )

        if os.path.isfile(path):
            if not self.empty_dir or self.recursive:
                self.alert(
                    "Cannot remove \'{}\': Is a directory".format(path),
                    Logger.ERROR,
                    NotFoundError
                )
        elif os.path.isdir(path):
            if not self.empty_dir:
                raise self.alert(
                    "Cannot remove \'{}\': Directory not empty".format(path),
                    Logger.ERROR,
                    NotEmptyError
                )
            elif not self.recursive and len(os.listdir(path)) != 0:
                raise self.alert(
                    "Cannot remove \'{}\': Directory not empty".format(path),
                    Logger.ERROR,
                    NotEmptyError
                )

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

        self.fs.move(path, path_in_trash)

        self._meta_add(path_in_trash, path)


    def _restore_item(self, item_name, item):
        path_in_trash = os.path.join(self.path, item_name)
        real_path = item.get("real_path")

        if os.path.exists(path_in_trash):
            self.fs.move(path_in_trash, real_path)
        else:
            self.logger.alert(
                "Can't found '{}' item in trash. It's lost.",
                Logger.ERROR,
                NotIndexedError
            )

        self._meta_remove(item_name)

    def _remove_item(self, name):
        path_in_trash = os.path.join(self.path, name)
        self.fs.remove(path_in_trash)
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

    def alert(self, message, message_type, error_type=None):
        if self.logger != None:
            self.logger.alert(message, message_type)

        if message_type == Logger.ERROR and error_type != None:
            if not self.force:
                raise error_type(message)
