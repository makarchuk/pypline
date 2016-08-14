from filter import Filter
class RemoveFilter(Filter):
    '''
    Simple filter for removing fields from event
    '''

    def __init__(self, fields):
        '''
        Accepts iterable of fields to remove
        '''
        self.fields = fields

    def filter(self, event):
        '''
        Filter implementation
        '''
        for field in self.fields:
            if field in event:
                del(event[field])
        return event

def test():
    rf = RemoveFilter(['a', 'b', 'c'])
    print rf.filter({'a': 1, 'b':2, 'd': 14})