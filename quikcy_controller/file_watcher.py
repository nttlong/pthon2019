
import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
class FileWatcher:
    def __init__(self, src_path,handler):
        self.__src_path = os.path.dirname(src_path)
        """
        patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        """
        self.__event_handler = PatternMatchingEventHandler(
            patterns= "*",
            ignore_directories= False,
            ignore_patterns= "",
            case_sensitive= False,
        )
        self.__event_handler.on_any_event=handler
        self.__event_observer = Observer()
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )
        self.__event_observer.start()

