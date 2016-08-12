from inputs import *
from filters import *
from outputs import *
from pypline import Pypline

config = {
    'inputs': [RandomInput({
                          "a": {"type": "int"},
                          "b": {"type": "int"},
                          "c": {"type": "str"}
                          })],
    'filters': [{'if': lambda ev: ev['a']<10,
                'filter': RemoveFilter(['a', 'b'])
                }],
    'outputs': [PrintOutput()]
}

Pypline(config).start()