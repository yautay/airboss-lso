import os.path
import time

from src.app import App
from src.lib.FileWatcher import FileWatcher

csv_path = os.path.join("C:\\", "repos", "airboss-lso", "tests", "csv")
watcher = FileWatcher(csv_path)
app = App()

if __name__ == "__main__":
    init_state = watcher.get_files()
    # app.run()
    while True:
        tick_state = watcher.get_files()
        new_files = watcher.list_comparer(init_state, tick_state)
        if new_files:
            print(f"NEW FILES RCVD: {new_files}")
            app.parse_csv_files(new_files)
        init_state = tick_state
        time.sleep(3)
