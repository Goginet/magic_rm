import os
import unittest
import shutil
import datetime
import time

from magic_rm.fs import SKIP, REPLACE
from  tests.general_test import TestGeneral, get_files_count
from magic_rm.trasher import MagicTrasher

class TestRestore(TestGeneral):
    def test_restore(self):
        before = get_files_count(self.BASE_DIR)
        trasher = MagicTrasher(path=self.TRASH_PATH, recursive=True)

        trasher.remove(self.BASE_DIR)
        self.assertEqual(os.path.exists(self.BASE_DIR), False)

        trasher.restore(os.path.basename(self.BASE_DIR))
        self.assertEqual(os.path.exists(self.BASE_DIR), True)
        self.assertEqual(get_files_count(self.BASE_DIR), before)

    def test_merge_skip_conflicts(self):
        default_str = "default"
        new_str = "new"

        trasher = MagicTrasher(path=self.TRASH_PATH, recursive=True, conflict_resolve=SKIP)

        with open(self.FILE_FOR_MERGE, 'w') as f:
            f.writelines(default_str)

        trasher.remove(self.BASE_DIR)

        os.makedirs(os.path.dirname(self.FILE_FOR_MERGE))
        with open(self.FILE_FOR_MERGE, 'w') as f:
            f.writelines(new_str)

        trasher.restore(os.path.basename(self.BASE_DIR))

        with open(self.FILE_FOR_MERGE, 'r') as f:
            now_str = f.readline()

        self.assertNotEqual(default_str, now_str)

    def test_merge_replace_conflicts(self):
        default_str = "default"
        new_str = "new"

        trasher = MagicTrasher(path=self.TRASH_PATH, recursive=True, conflict_resolve=REPLACE)

        with open(self.FILE_FOR_MERGE, 'w') as f:
            f.writelines(default_str)

        trasher.remove(self.BASE_DIR)

        os.makedirs(os.path.dirname(self.FILE_FOR_MERGE))
        with open(self.FILE_FOR_MERGE, 'w') as f:
            f.writelines(new_str)

        trasher.restore(os.path.basename(self.BASE_DIR))

        with open(self.FILE_FOR_MERGE, 'r') as f:
            now_str = f.readline()

        self.assertEqual(default_str, now_str)

    def test_add_remove_for_meta_file(self):
        item_name = os.path.basename(self.BASE_DIR)

        trasher = MagicTrasher(path=self.TRASH_PATH, recursive=True)

        trasher.remove(self.BASE_DIR)
        items = trasher.list_trash()
        self.assertEqual(items.has_key(item_name), True)

        trasher.restore(os.path.basename(self.BASE_DIR))
        items = trasher.list_trash()
        self.assertEqual(items.has_key(item_name), False)

    # def test_restore_from_trash_check_force_replace_dir(self):
    #     before = get_files_count(self.BASE_DIR)
    #     trasher = MagicTrasher(path=self.TRASH_PATH, force=True)
    #     trasher.move_to_trash(self.BASE_DIR)
    #     shutil.rmtree(self.BASE_DIR)
    #     build_dir(self.BASE_DIR)
    #     trasher.restore(os.path.basename(self.BASE_DIR))
    #     self.assertEqual(get_files_count(self.BASE_DIR), before)

    # def test_restore_from_trash_check_force_replace_file(self):
    #     before = get_files_count(self.BASE_DIR)
    #     trasher = MagicTrasher(path=self.TRASH_PATH, force=True)
    #     trasher.move_to_trash(self.BASE_DIR)
    #     shutil.rmtree(self.BASE_DIR)
    #     open(self.BASE_DIR, "w")
    #     trasher.restore(os.path.basename(self.BASE_DIR))
    #     self.assertEqual(get_files_count(self.BASE_DIR), before)

    # def test_restore_from_trash_check_meta(self):
    #     trasher = MagicTrasher(path=self.TRASH_PATH)
    #     trasher.move_to_trash(self.BASE_DIR)
    #     shutil.rmtree(self.BASE_DIR)
    #     trasher.restore(os.path.basename(self.BASE_DIR))
    #     items = trasher.list_trash()
    #     item_name = os.path.basename(self.BASE_DIR)
    #     self.assertEqual(items.has_key(item_name), False)

    # def test_restore_from_trash_check_trash(self):
    #     trasher = MagicTrasher(path=self.TRASH_PATH)
    #     trasher.move_to_trash(self.BASE_DIR)
    #     shutil.rmtree(self.BASE_DIR)
    #     trasher.restore(os.path.basename(self.BASE_DIR))
    #     path_in_trash = os.path.join(self.TRASH_PATH, os.path.basename(self.BASE_DIR))
    #     self.assertEqual(os.path.exists(path_in_trash), False)

if __name__ == '__main__':
    unittest.main()
