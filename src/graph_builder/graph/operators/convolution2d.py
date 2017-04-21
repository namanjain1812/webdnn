from typing import Dict, Tuple

from graph_builder.graph.graph import Operator, Variable
from graph_builder.graph.operators import attributes as A
from graph_builder.graph.variables import attributes as VA


class Convolution2D(Operator):
    """
    Convolutionレイヤー(bias含まず)
    """
    attributes = {A.PostElementwise,
                  A.PostAxiswise,
                  A.HaveWeights}

    def __init__(self, name: str, parameters: Dict[str, object]):
        """
        weights["W"]: (kh, kw, in_size, out_size)
        parameters: {ksize: Tuple[int, int], stride: Tuple[int, int], pad: Tuple[int, int]}
        :param name: 
        :param parameters: 
        """
        assert "ksize" in parameters
        assert "stride" in parameters
        assert "padding" in parameters
        super().__init__(name, parameters)

    def __call__(self, x: Variable, w: Variable):
        x_shape_dict = x.shape_dict
        w_shape_dict = w.shape_dict

        assert (w_shape_dict[A.Axis.H], w_shape_dict[A.Axis.W]) == self.ksize
        assert w_shape_dict[A.Axis.C] == x_shape_dict[A.Axis.C]

        N = x_shape_dict[A.Axis.N]
        H2 = (x_shape_dict[A.Axis.H] + 2 * self.PH - self.KH) // self.SH + 1
        W2 = (x_shape_dict[A.Axis.W] + 2 * self.PW - self.KW) // self.SW + 1
        C2 = w_shape_dict[A.Axis.N]

        if x.axis_order == VA.OrderNCHW:
            var_shape = [N, C2, H2, W2]
        elif x.axis_order == VA.OrderNHWC:
            var_shape = [N, H2, W2, C2]
        else:
            raise NotImplementedError()
        y = Variable(var_shape, x.axis_order)
        self.append_input("x", x)
        self.append_input("w", w)
        self.append_output("y", y)
        return y,

    @property
    def ksize(self) -> Tuple[int, int]:
        return self.parameters["ksize"]

    @property
    def stride(self) -> Tuple[int, int]:
        return self.parameters["stride"]

    @property
    def padding(self) -> Tuple[int, int]:
        return self.parameters["padding"]

    @property
    def KH(self) -> int:
        return self.ksize[0]

    @property
    def KW(self) -> int:
        return self.ksize[1]

    @property
    def SH(self) -> int:
        return self.stride[0]

    @property
    def SW(self) -> int:
        return self.stride[1]

    @property
    def PH(self) -> int:
        return self.padding[0]

    @property
    def PW(self) -> int:
        return self.padding[1]
