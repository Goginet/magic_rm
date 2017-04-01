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

    def setUp(self):
        self.mfs = mockfs.replace_builtins()

        self.mfs.add_entries({
            self.BASE_DIR: 'magic',
            self.BASE_DIR + "/dir1/a": 'magic',
            self.BASE_DIR + "/dir1/b": 'magic',
            self.BASE_DIR + "/dir1/dir2/a": 'magic2',
            self.BASE_DIR + "/dir3/e": 'magic'})

        self.mfs.makedirs(self.EMPTY_DIR)

    def tearDown(self):
        mockfs.restore_builtins()

    @access_patch
    def test_rmdir_empty(self):
        deleter = MagicDeleter(empty_dir=True)
        deleter.remove(self.EMPTY_DIR)
        self.assertEqual(os.path.exists(self.EMPTY_DIR), False)

    @access_patch
    def test_rmdir_recursive_base(self):
        deleter = MagicDeleter(recursive=True)
        deleter.remove(self.BASE_DIR)
        self.assertEqual(os.path.exists(self.BASE_DIR), False)

if __name__ == '__main__':
    unittest.main()
