from internal_queue import InternalQueue

class Output(object):
    def __init__(self):
        self.queue = InternalQueue(1000)

    def push(self, event):
        '''
        Called by output manager to push event to outputs personal queue
        '''
        self.queue.put(event)

    def finalize(self):
        '''
        Function being called before soft exit.
        TODO: Start runs in context which will handle finalize automatically.
        '''
        pass

    def set_exit_event(self, event):
        '''
        Function being called from pypeline. 
        Informs output which event it needs to listen
        '''
        self.exit_event = event

    def start(self):
        '''
        Main function.
        Runs in separate process generating taking
        events from personal queue and outputing then.
        You can skip this function in your outputs. It will work just fine as is
        '''
        while 1:
            if (self.exit_event.is_set() and self.queue.empty()):
                break                
            event = self.queue.safe_get()
            if event:
                self.output(event)
        self.finalize()

    def output(self, event):
        '''
        Outputs event
        '''
        pass

