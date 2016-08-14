class Input(object):
    def __init__(self):
        pass

    def set_queue(self, queue):
        self.queue = queue

    def set_exit_event(self, event):
        self.exit_event = event

    def start(self):
        while 1:
            event = self.generate()
            if event:
                try:
                    self.queue.put(event, False)
                    #logging.info("Event Emitted: {0}".format(event))
                except:
                    pass
