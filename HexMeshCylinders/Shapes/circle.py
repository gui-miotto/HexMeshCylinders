import math
from itertools import product
import numpy as np

from .shape2D import Shape2D, BoundingRectangle


class Circle(Shape2D):

    def __init__(self, diameter: float):
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
             layer_height of size height/n_layers meters. If n_layers=None, then n_layers
             will be equal to round(height/Cylinder.cell_edge), i.e. layer_height will be
             aproximatelly Cylinder.cell_edge.
        """

        if diameter <= 0:
            raise ValueError('diameter must be a positive number')

        self.radius = diameter / 2.

    @property
    def bounding_rectangle(self):
        br = BoundingRectangle(
            min_x=-self.radius,
            max_x=self.radius,
            min_y=-self.radius,
            max_y=self.radius,
        )
        return br

    def who_is_in(self, center_locations):
        ni, nj, _ = center_locations.shape
        isin = np.zeros((ni, nj), dtype=bool)
        for i, j in product(range(ni), range(nj)):
            [cx, cy] = center_locations[i, j]
            dist = (cx ** 2. + cy ** 2.) ** .5
            isin[i, j] = self.radius >= dist
        return isin

