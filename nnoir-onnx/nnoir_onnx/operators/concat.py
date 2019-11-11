import numpy as np
from nnoir.functions import *
from .utils import *


class OpConcat(Op):

    def __init__(self, node):
        super(OpConcat, self).__init__(node)

        self.axis = None
        for attr in node.attribute:
            if attr.name == 'axis':
                self.axis = attr.i

    def to_function(self, env, constants):
        return [
            Concat(
                list(self.node.input),
                list(self.node.output),
                axis=self.axis
            )
        ]
