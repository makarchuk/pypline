class Input():
    def __init__(queue):
        #TODO: set queue by set_queue method. not by __init__
        self.queue = queue

    def start():
        while 1:
            event = self.generate()
            if event:
                queue.put(event)