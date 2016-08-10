import random

class RandomInput():
    '''
    Generates random events by given description
    '''
    def __init__(self, structure={}):
        self.generation_mapping = {}
        for key in structure:
            value = structure[key]
            value_type = value['type']
            value_params = value
            gen_function = self.gen_func(value_type, value_params)
            self.generation_mapping[key] = gen_function

    def gen_func(self, type, options={}):
        '''
        Returns function which generate described field for event
        '''
        if type.lower() in ['int', 'integer']:
            return self.int_function(options)
        elif type.lower() in ['str', 'string']:
            return self.str_function(options)
        else:
            raise Exception("Unknown field type {0}".format(type))

    def int_function(self, options={}):
        '''
        Implementation of gen_func for type "int".
        Accepts 'max' and 'min' as extra parameters for random generation
        Default values are 10000 and 0 respectively
        Default values ironically chosen by random
        '''
        max = options.get('max', 10000)
        min = options.get('min', 0)
        return lambda : random.randint(min, max)

    def str_function(self, options={}):
        '''
        Implementation of gen_func for type "str"
        Accepts max_length and min_length extra parameters
        Default values are 0 and 100 respectively
        '''
        alphabet = 'abcdefghijklmnoprstuvwxyz '
        max = options.get('max_length', 100)
        min = options.get('min_length', 0)
        length = lambda min, max: random.randint(min, max)
        letter = lambda: random.choice(alphabet)
        return lambda: ('').join([letter() for x in range(length(min, max))])

    def generate(self):
        '''
        Returns random event
        '''
        res = {}
        for field in self.generation_mapping:
            res[field] = self.generation_mapping[field]()
        return res


def test():
    inp = RandomInput({'a': {'type': 'integer', 'max': 10},
                       'b': {'type': 'iNt', 'min': -10, 'max': 0},
                       'c': {'type': 'string','min_length':10,'max_length':20},
                       'd': {'type': 'string','max_length': 10}
                       })
    for x in range(1000):
        print inp.generate()
        #TODO: Check values, not just print them!