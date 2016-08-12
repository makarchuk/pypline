from multiprocessing import Queue, Process, Pool
import logging
logging.basicConfig(level=logging.DEBUG)

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
                self.filters.append((self._always_true, filter))
            else:
                self.filters.append((filter['if'], filter['filter']))
        self.outputs = []
        for output in config['outputs']:
            if 'output' in dir(output):
                self.outputs.append((self._always_true, output))
            else:
                self.outputs.append((output['if'], output['output']))

    def start(self):
        '''
        call all the methods required to propperly initiate pipeline
        '''
        self._init_queues()
        self._start_inputs_processes()
        self._start_filters_pool()
        self._start_output_manager_process()
        self._start_outputs_processes()

    def _init_queues(self):
        '''
        Init queues from inputs to filters and from filters to outputs
        '''

        self._input_to_filters_queue = Queue(maxsize=1000)
        for input in self.inputs:
            input.set_queue(self._input_to_filters_queue)
        self._filters_to_output_queue = Queue(maxsize=1000)

    def _start_outputs_processes(self):
        '''
        Start processes of each input
        Outputs must have method "start"
        which should generate events in a loop
        '''
        self.output_processes = []
        for condition, output in self.outputs:
            p = Process(target=output.start)
            self.output_processes.append(p)
            p.start()
        logging.info ("OUTPUTS PROCESSES STARTED!")

    def _start_inputs_processes(self):
        '''
        Start processes of each input
        Inputs must have method "start"
        which should generate events in a loop
        '''
        self.input_processes = []
        for input in self.inputs:
            p = Process(target=input.start)
            self.input_processes.append(p)
            p.start()
        logging.info ("INPUTS PROCESSES STARTED!")

    def _start_filters_pool(self):
        '''
        Creates number of processes.
        Each process runs throug queue and apply filtering function to events
        '''
        def _process():
            while 1:
                try:
                    event = self._input_to_filters_queue.get(False)
                except:
                    pass
                else:
                    self.filtering_function(event)

        self.filter_processes = []
        for x in range(10):
            p = Process(target=_process)
            self.filter_processes.append(p)
            p.start()

        logging.info ("FILTERS POOL STARTED!")

    def _start_output_manager_process(self):
        '''
        Runs a process for outputs_manager
        '''
        p = Process(target=self._outputs_manager)
        p.start()
        logging.info ("OUTPUT MANAGER STARTED!")

    def _outputs_manager(self):
        '''
        This function supposed to run in a separate process
        point of it is to take events from queue
        and give it to output processes
        It also handles conditional outputs
        '''
        while 1:
            try:
                event = self._filters_to_output_queue.get(False)
            except:
                #logging.info("EXCEPTION IN OUTPUT MANAGER! HOLY SHIT!")
                pass
            else:
                for condition, output in self.outputs:
                    if condition(event):
                        while 1:
                            try:
                                output.push(event)
                            except:
                                logging.info("Can't push event to output")
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
                logging.info("EXCEPTION IN FILTER")
                #TODO: Improve logging
        self._filters_to_output_queue.put(event, False)

if __name__ == '__main__':
    import config
    p = Pypline(config.config)
    p.start()