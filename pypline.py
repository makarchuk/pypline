class Pypline():
    def __init__(self, config):
        self.inputs = config['inputs']
        self.outputs = config['outputs']
        self.filters = []
        for filter in config['filters']:
            if 'filter' in dir(filter):
                self.fliters.append((self._never_skip_filter, filter))
            else:
                self.filters.append((filter['if'], filter['filter']))

    def _never_skip_filter(self, event):
        return True

    def filtering_function(self, event):
        for condition, filter in self.filters:
            try:
                if condition(event):
                    event = filter(event)
            except:
                pass
                #Some logging here!
        return event

