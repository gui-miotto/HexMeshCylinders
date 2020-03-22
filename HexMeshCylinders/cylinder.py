import numpy as np


class Cylinder():
    edge = None

    def __init__(self, diameter:int, height, n_layers):
        super().__init__()

        assert diameter % 2 == 1  # Diameter must be an odd integer
        assert Cylinder.edge is not None

        self.diam = diameter
        self.radius = diameter * Cylinder.edge / 2
        self.height = height
        self.n_layers = n_layers
        self.vertical_spacing = np.linspace(0, height, n_layers + 1)

    def who_is_in(self, base2dmesh):
        n = base2dmesh.shape[0]
        isin = np.zeros((n, n), dtype=bool)
        for i in range(n):
            for j in range(n):
                [cx, cy] = base2dmesh[i, j]
                dist = (cx ** 2. + cy ** 2.) ** .5
                isin[i, j] = self.radius >= dist
        return isin

