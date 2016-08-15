class Input(object):
    def __init__(self):
        import logging
        pass

    def set_queue(self, queue):
        self.queue = queue

    def set_exit_event(self, event):
        self.exit_event = event

    def finalize(self):
        pass

    def start(self):
        while 1:
            if self.exit_event.is_set():
                logging("EXITING!!!")
                break
            else:
                pass
            event = self.generate()
            if event:
                try:
                    self.queue.put(event, False)
                except:
                    pass
        self.finalize()