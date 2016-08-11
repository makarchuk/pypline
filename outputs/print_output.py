from output import Output
class PrintOutput(Output):
    '''
    Simple debugging output for printing events
    '''
    def __init__(self):
        super(self, PrintOutput).__init__()

    def output(self, event):
        print event
