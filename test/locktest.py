from threading import Lock
import time
import threading
__obj_lock__=1
my_lock=None
my_dict= {}
def test(x):
    global my_lock
    global my_dict
    if my_lock== None:
        my_lock = Lock()
    if my_dict.get(x,None) == None:
        my_lock.acquire()
        my_dict.update({x:0})
        print("Create new "+x)
        my_lock.release()

from re_egine import async_call

def get_result(ex,result):
    if ex!=None:
        print(ex)
    else:
        print(result)

import random
for i in range(0,1000):
    name="XX"+str(i%5)
    async_call.call_function(test,name).done(get_result)
