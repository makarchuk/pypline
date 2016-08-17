import multiprocessing.queues
import Queue

class InternalQueue(multiprocessing.queues.Queue):
    def __init__(self, *args, **kwargs):
        super(InternalQueue, self).__init__(*args, **kwargs)

    def safe_get(self, retries=10):
        for x in range(retries):
            try:
                element = self.get_nowait()
            except Queue.Empty:
                pass
            else:
                return element
