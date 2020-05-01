import math
from itertools import product
import numpy as np

from .shape2D import Shape2D, BoundingRectangle


class Ellipse(Shape2D):

    def __init__(self, len_x: float, len_y: float=None):
        if len_y is None:
            len_y = len_x

        if len_x <= 0 or len_y <= 0:
            raise ValueError('len_x and len_y must be a positive numbers')

        self.a = len_x / 2.
        self.b = len_y / 2.

    @property
    def bounding_rectangle(self):
        br = BoundingRectangle(
            min_x=-self.a,
            max_x=self.a,
            min_y=-self.b,
            max_y=self.b,
        )
        return br

    def who_is_in(self, center_locations):
        a2 = self.a ** 2.
        b2 = self.b ** 2.
        ni, nj, _ = center_locations.shape
        isin = np.zeros((ni, nj), dtype=bool)
        for i, j in product(range(ni), range(nj)):
            [cx, cy] = center_locations[i, j]
            dist = cx ** 2. / a2  + cy ** 2. / b2
            isin[i, j] = 1. >= dist
        return isin

