"""
This  module including:
    *set_root_dir   :set current directory
"""
import os
__root_dir__ = None

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