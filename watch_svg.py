import sys, json, time, logging, watchdog, websocket
from websocket import create_connection
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class SVGFileEventHandler(watchdog.events.FileSystemEventHandler):
    ws = None
    
    def on_modified(self, event):
        print(event.src_path)
        self.ws.send(json.dumps({"type": "modify", "path": event.src_path}))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = '.'
    
    event_handler = SVGFileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        ws = create_connection("ws://localhost:8888/svg")
        ws.connect("ws://localhost:8888/svg")
        event_handler.ws = ws
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

