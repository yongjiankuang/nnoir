from .function import Function


class Add(Function):
    def __init__(self, inputs, outputs, **params):
        required_params = set()
        optional_params = set()
        super(Add, self).__init__(inputs, outputs, params, required_params, optional_params)

    def run(self, x1, x2):
        return x1 + x2
