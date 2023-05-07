import os
import time
from os import listdir
from os.path import isfile, join


class FileWatcher(object):
    def __init__(self, path: str):
        self.path = path

    def get_files(self) -> list:
        files = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        return files

    @staticmethod
    def list_comparer(list_old: list, list_new: list) -> list[str]:
        diff = [x for x in list_new if
                x not in list_old]
        return diff
