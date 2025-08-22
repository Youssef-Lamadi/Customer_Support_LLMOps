import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import sys

# Get absolute path to project root (one level up from "infra")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.store_index import store_data_in_index

# path to your data folder
WATCH_FOLDER = os.path.join(PROJECT_ROOT, "data")


class DataChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"🔄 Change detected in: {event.src_path}")
            run_ingest()

    def on_created(self, event):
        if not event.is_directory:
            print(f"📂 New file detected: {event.src_path}")
            run_ingest()

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"🗑️ File deleted: {event.src_path}")
            run_ingest()

def run_ingest():
    print("🚀 Running ingestion pipeline...")
    store_data_in_index()
    print("Ingestion pipeline completed.")

if __name__ == "__main__":
    event_handler = DataChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=True)
    observer.start()

    print(f"👀 Watching folder: {WATCH_FOLDER} ...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
