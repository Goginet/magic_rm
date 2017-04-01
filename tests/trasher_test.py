import os
import unittest
import shutil
import datetime
import time

from mock import patch
import mockfs

from magic_rm.trasher import MagicTrasher

def get_files_count(path):
    count = 0
    for el in os.listdir(path):
        count += 1

    return count

def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate

def build_dir(path):
    os.makedirs(os.path.join(path, "dir1", "dir2"))
    os.makedirs(os.path.join(path, "dir3"))
    open(os.path.join(path, "dir1", "dir2", "a"), "w")
    open(os.path.join(path, "dir1", "dir2", "b"), "w")
    open(os.path.join(path, "dir3", "b"), "w")
    open(os.path.join(path, "dir3", "a"), "w")

@for_all_methods(patch("shutil.copymode", lambda x, y: None))
@for_all_methods(patch("shutil.copystat", lambda x, y: None))
class TestTrash(unittest.TestCase):

    TRASH_PATH = "/home/trash"

    BASE_DIR = "/long/long/path"
    EMPTY_DIR = BASE_DIR + "/empty"

    def setUp(self):
        self.mfs = mockfs.replace_builtins()

        self.mfs.add_entries({
            self.BASE_DIR + "/dir1/a": 'magic',
            self.BASE_DIR + "/dir1/b": 'magic',
            self.BASE_DIR + "/dir1/dir2/a": 'magic2',
            self.BASE_DIR + "/dir3/e": 'magic'})

        self.mfs.makedirs(self.EMPTY_DIR)

    def tearDown(self):
        mockfs.restore_builtins()

    def test_move_dir_to_trash_check_content(self):
        trasher = MagicTrasher(path=self.TRASH_PATH)
        trasher.move_to_trash(self.BASE_DIR)
        path_in_trash = os.path.join(self.TRASH_PATH, os.path.basename(self.BASE_DIR))
        self.assertEqual(get_files_count(path_in_trash), get_files_count(self.BASE_DIR))

    def test_move_dir_to_trash_check_meta(self):
        trasher = MagicTrasher(path=self.TRASH_PATH)
        trasher.move_to_trash(self.BASE_DIR)
        items = trasher.list_trash()
        item_name = os.path.basename(self.BASE_DIR)
        self.assertEqual(items.has_key(item_name), True)

    def test_move_dir_to_trash_check_retention(self):
        trasher = MagicTrasher(path=self.TRASH_PATH, retention=datetime.timedelta(seconds=1))
        trasher.move_to_trash(self.BASE_DIR)
        path_in_trash = os.path.join(self.TRASH_PATH, os.path.basename(self.BASE_DIR))
        time.sleep(1)
        trasher.flush()
        self.assertEqual(os.path.exists(path_in_trash), False)

    def test_restore_from_trash_check_content(self):
        before = get_files_count(self.BASE_DIR)
        trasher = MagicTrasher(path=self.TRASH_PATH)
        trasher.move_to_trash(self.BASE_DIR)
        shutil.rmtree(self.BASE_DIR)
        trasher.restore(os.path.basename(self.BASE_DIR))
        self.assertEqual(get_files_count(self.BASE_DIR), before)

    def test_restore_from_trash_check_force_replace_dir(self):
        before = get_files_count(self.BASE_DIR)
        trasher = MagicTrasher(path=self.TRASH_PATH, force=True)
        trasher.move_to_trash(self.BASE_DIR)
        shutil.rmtree(self.BASE_DIR)
        build_dir(self.BASE_DIR)
        trasher.restore(os.path.basename(self.BASE_DIR))
        self.assertEqual(get_files_count(self.BASE_DIR), before)

    def test_restore_from_trash_check_force_replace_file(self):
        before = get_files_count(self.BASE_DIR)
        trasher = MagicTrasher(path=self.TRASH_PATH, force=True)
        trasher.move_to_trash(self.BASE_DIR)
        shutil.rmtree(self.BASE_DIR)
        open(self.BASE_DIR, "w")
        trasher.restore(os.path.basename(self.BASE_DIR))
        self.assertEqual(get_files_count(self.BASE_DIR), before)

    def test_restore_from_trash_check_meta(self):
        trasher = MagicTrasher(path=self.TRASH_PATH)
        trasher.move_to_trash(self.BASE_DIR)
        shutil.rmtree(self.BASE_DIR)
        trasher.restore(os.path.basename(self.BASE_DIR))
        items = trasher.list_trash()
        item_name = os.path.basename(self.BASE_DIR)
        self.assertEqual(items.has_key(item_name), False)

    def test_restore_from_trash_check_trash(self):
        trasher = MagicTrasher(path=self.TRASH_PATH)
        trasher.move_to_trash(self.BASE_DIR)
        shutil.rmtree(self.BASE_DIR)
        trasher.restore(os.path.basename(self.BASE_DIR))
        path_in_trash = os.path.join(self.TRASH_PATH, os.path.basename(self.BASE_DIR))
        self.assertEqual(os.path.exists(path_in_trash), False)

if __name__ == '__main__':
    unittest.main()
