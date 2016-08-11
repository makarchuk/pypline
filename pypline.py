from multiprocessing import Queue, Process

class Pypline():
    def __init__(self, config):
        self.inputs = config['inputs']
        self.filters = []
        self._init_queues()
        # TODO: CONDITIONS TREE
        # 'if' :lambda
        # 'filter': filter
        # 'else': {Tree node!}

        for filter in config['filters']:
            if 'filter' in dir(filter):
                self.fliters.append((self._always_true, filter))
            else:
                self.filters.append((filter['if'], filter['filter']))
        self.outputs = []
        for otuput in config['otuputs']:
            if 'otuput' in dir(otuput):
                self.fliters.append((self._always_true, otuput))
            else:
                self.otuputs.append((otuput['if'], otuput['otuput']))

    def _init_queues(self):
        '''
        Init queues from inputs to filters and from filters to outputs
        '''

        self._input_to_filters_queue = Queue.Queue(maxsize=1000)
        self._filters_to_output_queue = Queue.Queue(maxsize=1000)

    def _start_inputs_processes(self):
        '''
        Start processes of each input
        Inputs must have method "start"
        which should generate events in a loop
        '''
        self.input_processes = []
        for input in self.inputs:
            p = Process(target=input.run,
                        kwargs={"queue" = self._input_to_filters_queue})
            self.input_processes.append(p)
            p.start()

    def _outputs_manager(self):
        '''
        This function supposed to run in a separate process
        point of it is to take events from queue
        and give it to output processes
        It also handles conditional outputs
        '''
        for condition, output in self.outputs:
            if condition(event):
                while 1:
                    try:
                        output.push(event)
                    except:
                        print("EXCEPTION OCCURED!")
                    else:
                        break

    def _always_true(self, event):
        '''
        stub to use as condition in unconditional outputs and filters
        '''
        return True

    def filtering_function(self, event):
        '''
        function which applies all the filters consecutively to an event
        '''
        for condition, filter in self.filters:
            try:
                if condition(event):
                    event = filter(event)
            except:
                pass
                #TODO: Some logging here!
        return event

