from output import Output

class PrintOutput(Output):
    '''
    Simple debugging output for printing events
    '''
    def __init__(self):
        self.counter = 0
        super(PrintOutput, self).__init__()

    def output(self, event):
        print ("{0}: {1}".format(self.counter, event))
        self.counter += 1
