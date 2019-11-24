"""
The application manager system
"""
import os
import json
from threading import Lock
from .file_watcher import FileWatcher
__lock__= None
__root_dir__ = None
__apps__ = None # dictionary of app info after read from file app.json
__apps_info__ = None # the cache of application info after convert from _apps__ dict
__on_config_change__ = [] # list of handle event when app json config change
def set_root_dir(dir):
   """
   Set current directory (Absolute Path of working directory)
   Note: The param dir in this method will be use calculate absolute path from relative path.
   Example: if you would like to get absolute full file path of a file place in app host
   :param dir:
   :return:
   """
   global __root_dir__
   __root_dir__ =  dir.replace('/',os.path.sep)
def on_apps_config_change(handler):
    global __on_config_change__
    __on_config_change__.append(handler)

def get_root_dir():
    """
    Get root directory of working app
    :return:
    """
    global __root_dir__
    if __root_dir__ == None:
        raise Exception("It looks like you forgot call {0}.set_root_dir".format(__name__))
    return  __root_dir__

def get_app_by_name(app_name):
    """Get application info by app name
    :return:ApplicationInfo
    """
    global __apps_info__
    global __lock__


    if __apps_info__ == None:
        load_apps("apps.json")
    return __apps_info__.get(app_name)

def get_all_apps():
    global __apps_info__
    global __lock__
    if __apps_info__ == None:
        load_apps("apps.json")
    return __apps_info__

def load_apps(json_config_file_path):
    """Load all applcation info and push to cache"""
    global __apps__
    global __apps_info__
    def handler(event):
        global __apps__
        global __apps_info__
        global __on_config_change__
        __apps__ = None
        __apps_info__ = None
        for h in __on_config_change__:
            h()


    if __apps__ == None:
        json_config_file_path=json_config_file_path.replace("/",os.path.sep)
        full_json_file_path = os.path.join(get_root_dir().replace("/",os.path.sep),json_config_file_path)
        FileWatcher(full_json_file_path, handler)
        with open(full_json_file_path) as json_file:
            json_text = json_file.read()
            __apps__ = json.loads(json_text)
            __apps_info__ = {}
            for k,v in __apps__.items():
                __apps_info__.update({k:ApplicationInfo(k,v)})
    return __apps_info__




class ApplicationInfo:
    def __init__(self,app_name,data):
        self.name = app_name
        self.__dict__ = data
        self.__dict__.update({
            "is_multi_tenancy":data.get("isMultiTenancy",False)
        })
        self.__dict__.update({
            "name": app_name
        })