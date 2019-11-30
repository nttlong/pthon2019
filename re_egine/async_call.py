import threading
class call_function (threading.Thread):
   def __init__(self, on_run,*args,**kwargs):
      threading.Thread.__init__(self)
      self.args=args
      self.result = None
      self.exception = None
      if callable(on_run):
          self.on_run=on_run
          self.args=args
          self.kwargs=kwargs
      else:
          raise ("on_run must be a func")
   def run(self):
       try:
           self.result=self.on_run(*self.args,**self.kwargs)
       except Exception as ex:
           self.exception=ex

   def done(self,on_done=None):
       self.run()
       if callable(on_done):
           on_done(self.exception, self.result)



