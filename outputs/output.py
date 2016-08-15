from multiprocessing import Queue

class Output(object):
    def __init__(self):
        self.queue = Queue(1000)

    def push(self, event):
        while 1:
            try:
                self.queue.put(event, False)
            except:
                logging.warn("Can't push to ouptut queue. It's probably full")
            else:
                break

    def finalize(self):
        pass

    def set_exit_event(self, event):
        self.exit_event = event

    def start(self):
        while 1:
            if (self.exit_event.is_set() and self.queue.empty()):
                break                
            try:
                event = self.queue.get(False)
            except Exception, e:
                pass
            else:
                self.output(event)
        self.finalize()

