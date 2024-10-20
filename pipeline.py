import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file uploaded: {event.src_path}")
            self.perform_action(event.src_path)

    def perform_action(self, file_path):
        with open(file_path, "r") as file:
            content = file.read()
            print(content)


def start_watching(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    folder_to_watch = "./demands"
    start_watching(folder_to_watch)
