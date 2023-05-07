import os.path
import time

from src.app import App
from src.lib.FileWatcher import FileWatcher

csv_path = os.path.join("C:", "repos", "airboss-lso", "tests", "csv")

watcher = FileWatcher(csv_path)
app = App()

if __name__ == "__main__":
    state = watcher.get_files()
    app.run()
    while True:
        new_files = watcher.list_comparer(state, watcher.get_files())
        if new_files:
            print(f"NEW FILES RCVD: {new_files}")
            app.got_csv_files(new_files)
        state = new_files
        time.sleep(10)
