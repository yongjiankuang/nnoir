from chainer.functions.math.basic_math import Add, AddConstant, Mul, MulConstant
from mlir_chainer.patch import patched_function_apply, patched_function_call

if hasattr(Add, 'apply'):
    Add.apply = patched_function_apply(Add.apply)
else:
    Add.__call__ = patched_function_call(Add.__call__)

def to_mlir_node(self):
    return {
        b'name': 'Add',
        b'params': {}
    }
Add.to_mlir_node = to_mlir_node

if hasattr(AddConstant, 'apply'):
    AddConstant.apply = patched_function_apply(AddConstant.apply)
else:
    AddConstant.__call__ = patched_function_call(AddConstant.__call__)

def to_mlir_node(self):
    return {
        b'name': 'AddConstant',
        b'params': {
            b'value': float(self.value)
        }
    }
AddConstant.to_mlir_node = to_mlir_node

if hasattr(Mul, 'apply'):
    Mul.apply = patched_function_apply(Mul.apply)
else:
    Mul.__call__ = patched_function_call(Mul.__call__)

def to_mlir_node(self):
    return {
        b'name': 'Mul',
        b'params': {}
    }
Mul.to_mlir_node = to_mlir_node

if hasattr(MulConstant, 'apply'):
    MulConstant.apply = patched_function_apply(MulConstant.apply)
else:
    MulConstant.__call__ = patched_function_call(MulConstant.__call__)

def to_mlir_node(self):
    return {
        b'name': 'MulConstant',
        b'params': {
            b'value': float(self.value)
        }
    }
MulConstant.to_mlir_node = to_mlir_node