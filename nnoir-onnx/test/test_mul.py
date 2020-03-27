from util import Base
from onnx import TensorProto
from onnx.helper import make_node, make_graph, make_model, make_tensor_value_info, make_tensor, make_opsetid
from onnx.numpy_helper import from_array
import onnx
import numpy as np

from nnoir_onnx.operators.utils import UnsupportedONNXOperation
from nose.tools import raises

info = make_tensor_value_info


def test_mul_00():
    '''
    opset version >= 7
    without constant, supports multidirectional broadcasting
    '''

    a_shape = (1, 1, 3, 4)
    b_shape = (1, 2, 3, 1)
    out_shape = (1, 2, 3, 4)

    class MulTester(Base):
        def create_onnx(self) -> onnx.ModelProto:
            node = make_node("Mul", inputs=["A", "B"], outputs=["C"])
            inputs = [info("A", TensorProto.FLOAT, a_shape), info("B", TensorProto.FLOAT, b_shape)]
            outputs = [info("C", TensorProto.FLOAT, out_shape)]

            graph = make_graph([node], "add_graph", inputs, outputs)
            model = make_model(graph)
            return model

    a = np.random.rand(*a_shape).astype(np.float32)
    b = np.random.rand(*b_shape).astype(np.float32)

    outputs = ["C"]
    MulTester({"A": a, "B": b}, outputs).run()


@raises(UnsupportedONNXOperation)
def test_mul_01():
    '''
    opset version >= 7
    with one constant, does not support multidirectional broadcasting
    '''

    a_shape = (1, 1, 3, 4)
    b_shape = (1, 2, 3, 1)
    out_shape = (1, 2, 3, 4)

    class MulTester(Base):
        def create_onnx(self) -> onnx.ModelProto:
            node = make_node("Mul", inputs=["A", "B"], outputs=["C"])
            inputs = [info("A", TensorProto.FLOAT, a_shape)]
            outputs = [info("C", TensorProto.FLOAT, out_shape)]

            B = np.random.rand(*b_shape).astype(np.float32)

            b_init = from_array(B, "B")
            graph = make_graph([node], "add_graph", inputs, outputs, initializer=[b_init])
            model = make_model(graph)
            return model

    a = np.random.rand(*a_shape).astype(np.float32)

    outputs = ["C"]
    MulTester({"A": a}, outputs).run()


def test_mul_02():
    '''
    opset version <= 6

    support axis attribute
    '''

    a_shape = (1, 2, 3, 4)
    b_shape = (2, 3)
    out_shape = (1, 2, 3, 4)

    class MulTester(Base):
        def create_onnx(self) -> onnx.ModelProto:
            node = make_node("Mul", inputs=["A", "B"], outputs=["C"], axis=1, broadcast=1)
            inputs = [info("A", TensorProto.FLOAT, a_shape), info("B", TensorProto.FLOAT, b_shape)]
            outputs = [info("C", TensorProto.FLOAT, out_shape)]

            graph = make_graph([node], "add_graph", inputs, outputs)
            model = make_model(graph, opset_imports=[make_opsetid("", 6)])
            return model

    a = np.random.rand(*a_shape).astype(np.float32)
    b = np.random.rand(*b_shape).astype(np.float32)

    outputs = ["C"]
    MulTester({"A": a, "B": b}, outputs).run()


def test_mul_03():
    '''
    opset version <= 6

    support axis attribute with one constant
    '''

    a_shape = (1, 2, 3, 4)
    b_shape = (2, 3)
    out_shape = (1, 2, 3, 4)

    class MulTester(Base):
        def create_onnx(self) -> onnx.ModelProto:
            node = make_node("Mul", inputs=["A", "B"], outputs=["C"], axis=1, broadcast=1)
            inputs = [info("A", TensorProto.FLOAT, a_shape)]
            outputs = [info("C", TensorProto.FLOAT, out_shape)]

            B = np.random.rand(*b_shape).astype(np.float32)

            b_init = from_array(B, "B")
            graph = make_graph([node], "add_graph", inputs, outputs, initializer=[b_init])
            model = make_model(graph, opset_imports=[make_opsetid("", 1)])
            return model

    a = np.random.rand(*a_shape).astype(np.float32)

    outputs = ["C"]
    MulTester({"A": a}, outputs).run()
