import os
import shutil
from root import ROOT_DIR

folders = [
    os.path.join(ROOT_DIR, "tests", "results", "funkman"),
    os.path.join(ROOT_DIR, "tests", "results", "yautay"),
    os.path.join(ROOT_DIR, "tests", "results", "data")
]

for folder in folders:
    for filename in os.listdir(folder):
        if filename != ".gitkeep":
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
