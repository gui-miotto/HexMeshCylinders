import math
from itertools import product
import numpy as np


class Cylinder():

    cell_edge = None

    def __init__(self, diameter:int, height:float, n_layers:int):
        """ Specifies a cylinder to be used to create the final volume (a stack of cylinders).

        Parameters
        ----------
        diameter : int
            Diameter of cylinder specified in cell edeges. Basically it tells how many
             cells will fit inside the cylinder diameter. This number must be odd
             because the axis of the cylinder contains the center of the central cell
             of each layer.
        height : float
            Height of the cylinder in meters.
        n_layers : int
            Into how many layers will the cylinder be divided. All layers will have equal
             layer_height of size height/n_layers meters.
        """

        if type(diameter) is not int:
            raise TypeError('diameter must be an integer')
        if diameter % 2 != 1 and diameter > 0:
            raise ValueError('diameter must be a positive odd number')
        if Cylinder.cell_edge is None:
            raise AttributeError('A value for Cylinder.edge must be given')

        self.diameter = diameter
        self.radius = diameter * Cylinder.cell_edge / 2.
        self.height = height
        self.n_layers = n_layers
        self.vertical_spacing = np.linspace(0, height, n_layers + 1)

    def who_is_in(self, center_locations):
        #TODO: can be improved by symmetry
        ni, nj, _ = center_locations.shape
        isin = np.zeros((ni, ni), dtype=bool)
        for i, j in product(range(ni), range(ni)):
            [cx, cy] = center_locations[i, j]
            dist = (cx ** 2. + cy ** 2.) ** .5
            isin[i, j] = self.radius >= dist
        return isin

    @classmethod
    def conv_diam(cls, diam_in_meters:float):
        """Converts a diameter given in meters to a diameter given in a valid number of
         cell edeges

        Parameters
        ----------
        diam_in_meters : float
            Diameter given in meters

        Returns
        -------
        int
            Diameter given in cell edges. The number will be odd as required.
        """
        if cls.cell_edge is None:
            raise AttributeError('A value for Cylinder.edge must be given')

        float_edges = diam_in_meters / cls.cell_edge
        int_edges = int(round(float_edges))
        if math.modf(float_edges)[0] > .5:
            return int_edges - 1 if int_edges % 2 == 0 else int_edges
        else:
            return int_edges + 1 if int_edges % 2 == 0 else int_edges