from tests.csv.path import CSV_DIR
from src.lib.FileWatcher import FileWatcher

watcher = FileWatcher(CSV_DIR)
xx = watcher.start_watcher()


