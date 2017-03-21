import os
import unittest

from mock import patch
import mockfs

from magic_rm.deleter import MagicDeleter


def assert_alert(message):
    def _decorator(func):
        def wrapper(self):
            with patch("magic_rm.deleter.MagicDeleter.alert") as alert_mock:
                func(self)
                alert_mock.assert_called_with(message)
            return func(self)
        return wrapper
    return _decorator

def access_patch(decorate_func):
    def access(path, mode):
        return True

    def wrapper(self):
        with patch("os.access", access):
            decorate_func(self)

    return wrapper

class TestRemove(unittest.TestCase):

    BASE_DIR = "/long/long/path"
    EMPTY_DIR = BASE_DIR + "/empty"
    FILL_DIR = BASE_DIR + "/fill"
    FILES_LIST = ["a", "b", "c"]

    def setUp(self):
        self.mfs = mockfs.replace_builtins()

        entries = {}
        for f in self.FILES_LIST:
            entries.update(dict([(os.path.join(self.FILL_DIR, f), 'file')]))

        self.mfs.add_entries(entries)
        self.mfs.makedirs(self.EMPTY_DIR)

    def tearDown(self):
        mockfs.restore_builtins()

    @access_patch
    def test_rmdir_empty(self):
        deleter = MagicDeleter(empty_dir=True, recursive=False, interactive=False, force=False)
        deleter.remove(self.EMPTY_DIR)
        self.assertEqual(os.path.exists(self.EMPTY_DIR), False)

    @access_patch
    def test_rmdir_recursive_base(self):
        deleter = MagicDeleter(empty_dir=False, recursive=True, interactive=False, force=False)
        deleter.remove(self.BASE_DIR)
        self.assertEqual(os.path.exists(self.BASE_DIR), False)

    @access_patch
    @assert_alert("Cannot remove '{}': Directory not empty".format(BASE_DIR))
    def test_rmdir_not_empty_check_err(self):
        deleter = MagicDeleter(empty_dir=True, recursive=False, interactive=False, force=False)
        deleter.remove(self.BASE_DIR)

    @access_patch
    @assert_alert("Cannot remove '{}': Is a directory".format(BASE_DIR))
    def test_rmdir_not_dir_check_err(self):
        deleter = MagicDeleter(empty_dir=False, recursive=False, interactive=False, force=False)
        deleter.remove(self.BASE_DIR)

if __name__ == '__main__':
    unittest.main()
