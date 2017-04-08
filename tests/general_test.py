import unittest

import os
from os.path import join, exists
from pyfakefs import fake_filesystem_unittest

def get_files_count(path):
    count = 0
    for el in os.listdir(path):
        count += 1

    return count

class TestGeneral(fake_filesystem_unittest.TestCase):

    TRASH_PATH = "/trash"
    BASE_DIR = "/long/long/path"
    NOT_FOUND = join(BASE_DIR, "bad/bad/soooooo bad")
    EMPTY_DIR = join(BASE_DIR, "empty")

    FILE_FOR_MERGE = join(BASE_DIR, "merge_file")

    REGEXP_POSTFIX = ".regexp"

    REGEXP_DIRS = [
        join(BASE_DIR, "regexp1"),
        join(BASE_DIR, "regexp2"),
        join(BASE_DIR, "regexp2", "regexp3"),
    ]

    REGEXP_FILES = [
        join(BASE_DIR, "file11." + REGEXP_POSTFIX),
        join(BASE_DIR, "file12." + REGEXP_POSTFIX),
        join(REGEXP_DIRS[0], "file21." + REGEXP_POSTFIX),
        join(REGEXP_DIRS[1], "file31." + REGEXP_POSTFIX),
        join(REGEXP_DIRS[1], "file32." + REGEXP_POSTFIX),
        join(REGEXP_DIRS[2], "file41." + REGEXP_POSTFIX),
        join(REGEXP_DIRS[2], "file42." + REGEXP_POSTFIX),
    ]

    def setUp(self):
        self.setUpPyfakefs()

        self.fs.CreateDirectory(self.BASE_DIR)
        self.fs.CreateDirectory(self.EMPTY_DIR)
        self.fs.CreateDirectory(join(self.BASE_DIR, "dir1"))
        self.fs.CreateDirectory(join(self.BASE_DIR, "dir1", "dir2"))


        self.fs.CreateFile(join(self.BASE_DIR, "dir1", "a"))
        self.fs.CreateFile(join(self.BASE_DIR, "dir1", "b"))
        self.fs.CreateFile(join(self.BASE_DIR, "dir1", "dir2", "a"))
        self.fs.CreateFile(join(self.BASE_DIR, "dir3", "e"))

        for path in self.REGEXP_DIRS:
            if not exists(path):
                self.fs.CreateDirectory(path)

        for path in self.REGEXP_FILES:
            self.fs.CreateFile(path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
