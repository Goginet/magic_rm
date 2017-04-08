#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

import os
import shutil
import threading
import time

from magic_rm.errors import NotEmptyError
from magic_rm.walker import Logger, MagicWalker

SKIP = "SKIP"
REPLACE = "REPLACE"

RESTORE_MODES = [SKIP, REPLACE]


class MagicFs(object):

    def __init__(self,
                 progress=False,
                 force=False,
                 interactive=False,
                 recursive=False,
                 empty_dir=False,
                 regexp=None,
                 symlinks=False,
                 conflict=REPLACE,
                 logger=None):

        self.regexp = regexp
        self.conflict = conflict
        self.progress = progress
        self.force = force
        self.interactive = interactive
        self.recursive = recursive
        self.empty_dir = empty_dir
        self.logger = logger
        self.symlinks = symlinks

        self.walker = MagicWalker(
            force=self.force,
            regexp=self.regexp,
            recursive=self.recursive,
            symlinks=self.symlinks,
        )

    def move(self, src, dst):
        self.copy(src, dst)
        self.remove(src)

    def remove(self, path):
        def remove_link(path):
            self._remove_symlink(path)

        def remove_file(path):
            self._remove_file(path)

        def remove_dir(path):
            self._remove_dir(path)

        self.walker.link_handler = remove_link
        self.walker.file_handler = remove_file
        self.walker.after_go_to_dir_handler = remove_dir

        self.walker.walk(path)

    def copy(self, src, dst):

        def copy_link(path):
            if path == src:
                self._copy_symlink(path, dst)
            else:
                relpath = os.path.relpath(path, src)
                new_dest = os.path.join(dst, relpath)

                self._copy_symlink(path, new_dest)

        def copy_file(path):
            if path == src:
                self._copy_file(path, dst)
            else:
                relpath = os.path.relpath(path, src)
                new_dest = os.path.join(dst, relpath)

                self._copy_file(path, new_dest)

        def copy_dir(path):
            if path == src:
                self._copy_dir(path, dst)
            else:
                relpath = os.path.relpath(path, src)
                new_dest = os.path.join(dst, relpath)

                self._copy_dir(path, new_dest)

        if self.symlinks:
            copy_link = None

        walker = MagicWalker(
            force=self.force,
            recursive=self.recursive,
            symlinks=self.symlinks,
            link_handler=copy_link,
            file_handler=copy_file,
            regexp=self.regexp,
            before_go_to_dir_handler=copy_dir
        )

        self.walker.link_handler = copy_link
        self.walker.file_handler = copy_file
        self.walker.after_go_to_dir_handler = copy_dir

        walker.walk(src)

    def _copy_symlink(self, src, dst):
        self._build_dest(dst)
        self.__alert("copy symlink \'{}\', to \'{}\'".format(src, dst), Logger.INFO)
        linkto = os.readlink(src)
        os.symlink(linkto, dst)

    def _copy_file(self, src, dst):
        self._build_dest(dst)

        if os.path.exists(dst):
            if self.conflict == REPLACE and os.path.isfile(dst):
                self.__alert("replace file \'{}\', to \'{}\'".format(dst, src), Logger.INFO)
                self.__copy_file(src, dst)
        else:
            self.__alert("copy file \'{}\', to \'{}\'".format(src, dst), Logger.INFO)
            self.__copy_file(src, dst)

    def _copy_dir(self, src, dst):
        self._build_dest(dst)

        if not os.path.exists(dst):
            self.__alert("copy dir \'{}\', to \'{}\'".format(src, dst), Logger.INFO)
            os.mkdir(dst)

    def _build_dest(self, path):
        dest = os.path.dirname(path)
        if not os.path.exists(dest):
            os.makedirs(dest)

    def _remove_symlink(self, path):
        self.__alert("remove symlink \'{}\'".format(path), Logger.INFO)
        self.__unlink(path)

    def _remove_file(self, path):
        self.__alert("remove file \'{}\'".format(path), Logger.INFO)
        self.__rmfile(path)

    def _remove_dir(self, path):
        self.__alert("remove dir \'{}\'".format(path), Logger.INFO)
        if len(os.listdir(path)) == 0:
            self.__rmdir(path)
        else:
            raise self.__alert("Cannot remove \'{}\': Directory not empty".format(path),
                               Logger.ERROR, NotEmptyError)

    def __unlink(self, path):
        os.unlink(path)

    def __rmdir(self, path):
        os.rmdir(path)

    def __copy_file(self, src, dst):
        if self.progress:
            MagicFs.__run_task(
                task=lambda: shutil.copyfile(src, dst),
                total_size=os.path.getsize(src),
                get_now_size=lambda: os.path.getsize(dst),
            )
        else:
            shutil.copyfile(src, dst)

    def __rmfile(self, path):
        if self.progress:
            MagicFs.__run_task(
                task=lambda: os.remove(path),
                total_size=os.path.getsize(path),
                get_now_size=lambda: os.path.getsize(path),
            )
        else:
            os.remove(path)

    @staticmethod
    def __run_task(task, total_size, get_now_size):
        PROGRESS_SIZE = 100
        def print_progress(now_size):
            progress = int((float(now_size + 1) / (total_size + 1)) * PROGRESS_SIZE)
            print("{}>{}|{}".format("-" * progress, " " * (PROGRESS_SIZE - progress), "\033[F"))

        worker = threading.Thread(target=task)
        worker.start()
        time.sleep(0.01)

        while worker.isAlive():
            try:
                now_size = get_now_size()
            except Exception:
                return

            time.sleep(0.5)

            print_progress(now_size)
        print_progress(total_size)
        print

    def __alert(self, message, message_type, error_type=None):
        if self.logger != None:
            self.logger.alert(message, message_type)

        if message_type == Logger.ERROR and error_type != None:
            if not self.force:
                raise error_type(message)
