import math
from itertools import product
import numpy as np

from .shape2D import Shape2D, BoundingRectangle


class Circle(Shape2D):

    def __init__(self, diameter: float):
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

