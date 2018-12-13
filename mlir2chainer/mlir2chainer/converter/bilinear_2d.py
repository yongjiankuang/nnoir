import chainer.functions as F

class ConvertBilinear2D():
    def to_chainer(self, edge, x):
        return F.resize_images(x, tuple(edge.params['size']))
