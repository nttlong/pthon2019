"""
This  module including:
    *set_root_dir   :set current directory
"""
import os
import json
__root_dir__ = None
__apps__ = None
__apps_info__ = None
def set_root_dir(dir):
   """
   Set current directory (Absolute Path of working directory)
   Note: The param dir in this method will be use calculate absolute path from relative path.
   Example: if you want to get absolute full file path of a file place in app host
   :param dir:
   :return:
   """
   global __root_dir__
   __root_dir__ =  dir

def get_root_dir():
    """
    Get root directory of working app
    :return:
    """
    global __root_dir__
    if __root_dir__ == None:
        raise Exception("It looks like you forgot call {0}.set_root_dir".format(__name__))
    return  __root_dir__

class ApplicationInfo:
    def __init__(self,app_name,data):
        self.name = app_name
        self.__dict__ = data



def load_apps(json_config_file_path):
    """Load all applcation info and push to cache"""
    global __apps__
    global __apps_info__
    if __apps__ == None:
        full_json_file_path = os.path.join(get_root_dir(),json_config_file_path)
        with open(full_json_file_path) as json_file:
            json_text = json_file.read()
            __apps__ = json.loads(json_text)
            __apps_info__ = {}
            for k,v in __apps__.items():
                __apps_info__.update({k:ApplicationInfo(k,v)})
    return __apps_info__

def get_app(app_name):
    global __apps_info__
    if __apps_info__ == None:
        load_apps("apps.json")
    return  __apps_info__.get(app_name)

