class Input(object):
    def __init__(self):
        pass

    def set_queue(self, queue):
        '''
        Function being called from pypeline. 
        Informs input where to put generated events
        '''
        self.queue = queue

    def set_exit_event(self, event):
        '''
        Function being called from pypeline. 
        Informs input which event it needs to listen
        '''
        self.exit_event = event

    def finalize(self):
        '''
        Function being called before soft exit.
        TODO: Start runs in context which will handle finalize automatically.
        '''
        pass

    def start(self):
        '''
        Main function.
        Runs in separate process generating new events.
        You can skip this function in your inputs. It will work just fine as is
        '''
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
    
    def generate(self):
        '''
        Function called to generate new event
        needs to be implemented in real inputs
        '''
        pass