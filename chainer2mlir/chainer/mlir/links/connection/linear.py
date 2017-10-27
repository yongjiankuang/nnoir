import chainer
import chainer.links as links
from chainer.mlir import node
from chainer.mlir.node import encode_ndarray

class Linear(node.Link, links.Linear):
    def __init__(self, *inputs, **dicts):
        super(Linear, self).__init__(links.Linear)
        super(node.Link, self).__init__(*inputs, **dicts)

    def to_mlir_node(self):
        return {
            b'name': self.chainer_node_label,
            b'params': {
                b'W': encode_ndarray(self.W.data),
                b'b': encode_ndarray(self.b.data)
            }
        }
