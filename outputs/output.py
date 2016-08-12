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


    def start(self):
        while 1:
            try:
                event = self.queue.get(False)
            except Exception, e:
                #print "No events yet!"
                pass
            else:
                self.output(event)

