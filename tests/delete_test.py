import os
import unittest

from  tests.general_test import TestGeneral

from magic_rm.trasher import MagicTrasher
from magic_rm.errors import NotFoundError, NotEmptyError


class TestRemove(TestGeneral):

    def test_remove_raise_not_found(self):
        trasher = MagicTrasher()
        with self.assertRaises(NotFoundError):
            trasher.remove(self.NOT_FOUND)

    def test_remove_raise_not_empty(self):
        trasher = MagicTrasher(recursive=False)
        with self.assertRaises(NotEmptyError):
            trasher.remove(self.BASE_DIR)

    def test_remove_recursive_regex(self):
        REGEXP = ".*\\.regexp"
        trasher = MagicTrasher(recursive=True, regexp=REGEXP, force=True)
        trasher.remove(self.BASE_DIR)
        self.assertEqual(os.path.exists(self.BASE_DIR), True)
        for path in self.REGEXP_DIRS:
            self.assertEqual(os.path.exists(path), False)
        for path in self.REGEXP_DIRS:
            self.assertEqual(os.path.exists(path), False)

    def test_move_to_trash(self):
        trasher = MagicTrasher(recursive=True, path=self.TRASH_PATH)
        trasher.remove(self.BASE_DIR)

        path_in_trash = os.path.join(self.TRASH_PATH, os.path.basename(self.BASE_DIR))
        self.assertEqual(os.path.exists(path_in_trash), True)

    def test_move_to_trash_incriment(self):
        trasher = MagicTrasher(recursive=True, path=self.TRASH_PATH)
        trasher.remove(self.BASE_DIR)
        os.makedirs(self.BASE_DIR)
        trasher.remove(self.BASE_DIR)

        path_in_trash = os.path.join(self.TRASH_PATH, os.path.basename(self.BASE_DIR))
        path_incriment = "{}_(1)".format(path_in_trash)
        self.assertEqual(os.path.exists(path_incriment), True)

    def test_remove_recursive(self):
        trasher = MagicTrasher(recursive=True)
        trasher.remove(self.BASE_DIR)
        self.assertEqual(os.path.exists(self.BASE_DIR), False)

if __name__ == '__main__':
    unittest.main()
