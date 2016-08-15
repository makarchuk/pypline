from output import Output
import logging

class PrintOutput(Output):
    '''
    Simple debugging output for printing events
    '''
    def __init__(self):
        self.counter = 0
        super(PrintOutput, self).__init__()

    def output(self, event):
        logging.info("OUTPUT #{0}: {1}".format(self.counter, event))
        self.counter += 1
