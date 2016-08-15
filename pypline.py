from multiprocessing import Queue, Process
import multiprocessing
import logging
import sys
import os

logging.basicConfig(level=logging.INFO)

class Pypline():
    def __init__(self, config):
        self.inputs = config['inputs']
        self.filters = []
        self.exiting_event = multiprocessing.Event()
        self.outputs_exiting_event = multiprocessing.Event()
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
        with self.runner_context():
            self._init_queues_and_events()
            self._start_inputs_processes()
            self._start_filters_pool()
            self._start_output_manager_process()
            self._start_outputs_processes()
            self._wait_for_signals()

    def runner_context(self):
        return RunnerContext(self)

    def soft_exit(self, *args):
        logging.info("SOFT_EXIT!")
        self.exiting_event.set()
        [p.join() for p in self.input_processes]
        logging.info("INPUTS JOINED")
        self.outputs_manager_process.join()
        logging.info("OUTPUTS MANAGER JOINED")
        [p.join() for p in self.filter_processes]
        logging.info("FILTERS JOINED")
        self.outputs_exiting_event.set()
        [p.join() for p in self.output_processes]
        logging.info("OUTPUTS JOINED")
        sys.exit()

    def hard_exit(self, *args):
        logging.info("HARD EXIT!")
        [p.terminate() for p in self.input_processes]
        [p.join() for p in self.input_processes]
        logging.info("INPUTS TERMINATED")
        self.outputs_manager_process.terminate()
        self.outputs_manager_process.join()
        logging.info("OUTPUTS MANAGER TERMINATED")
        [p.terminate() for p in self.filter_processes]
        [p.join() for p in self.filter_processes]
        logging.info("FILTERS TERMINATED")
        self.outputs_exiting_event.set()
        [p.terminate() for p in self.output_processes]
        [p.join() for p in self.output_processes]
        logging.info("OUTPUTS TERMINATED")
        sys.exit()

    def _wait_for_signals(self):
        '''
        Wait for sigterm or sigkill or for KeyboardInterrupt exception
        to properly kill al the processes
        '''

        import signal
        import time
        import os

        signal.signal(signal.SIGTERM, self.hard_exit)
        while 1:
            time.sleep(1)




    def _init_queues_and_events(self):
        '''
        Init queues from inputs to filters and from filters to outputs
        '''
        self._input_to_filters_queue = Queue(maxsize=1000)
        self._filters_to_output_queue = Queue(maxsize=1000)

        for input in self.inputs:
            input.set_queue(self._input_to_filters_queue)
            input.set_exit_event(self.exiting_event)
        for condition, output in self.outputs:
            output.set_exit_event(self.outputs_exiting_event)


    def _start_outputs_processes(self):
        '''
        Start processes of each input
        Outputs must have method "start"
        which should generate events in a loop
        '''
        self.output_processes = []
        for condition, output in self.outputs:
            p = Process(target=output.start, name=output.__class__.__name__)
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
            p = Process(target=input.start, name=input.__class__.__name__)
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
                if (self.exiting_event.is_set() and
                            self._input_to_filters_queue.empty()):
                    break
                    logging.info("FILTERS EXITED")
                try:
                    event = self._input_to_filters_queue.get(False)
                except:
                    pass
                else:
                    self.filtering_function(event)

        self.filter_processes = []
        for x in range(5):
            p = Process(target=_process, name="Filter")
            self.filter_processes.append(p)
            p.start()

        logging.info ("FILTERS POOL STARTED!")

    def _start_output_manager_process(self):
        '''
        Runs a process for outputs_manager
        '''
        p = Process(target=self._outputs_manager, name="OutputManager")
        p.start()
        self.outputs_manager_process=p
        logging.info ("OUTPUT MANAGER STARTED!")

    def _outputs_manager(self):
        '''
        This function supposed to run in a separate process
        point of it is to take events from queue
        and give it to output processes
        It also handles conditional outputs
        '''
        while 1:
            if (self.exiting_event.is_set() and
                    self._filters_to_output_queue.empty()):
                break
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
                                pass
                                #logging.info("Can't push event to output")
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
        while 1:
            try:
                self._filters_to_output_queue.put(event, False)
            except:
                pass
            else:
                break

class RunnerContext():
    def __init__(self, pypeline):
        self.pypeline = pypeline

    def __enter__(self):
        pid = os.getpid()
        with open('pypeline.pid', 'w') as f:
            f.write(str(pid))

    def __exit__(self, type, exc, bt):
        os.remove('pypeline.pid')
        #TODO: Handle different exception types different way
        self.pypeline.soft_exit()

if __name__ == '__main__':
    import config
    p = Pypline(config.config)
    p.start()
