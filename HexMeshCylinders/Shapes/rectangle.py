from itertools import product

import numpy as np

from .shape2D import Shape2D, BoundingRectangle


class Rectangle(Shape2D):

    def __init__(self, len_x: float, len_y: float=None):
        if len_y is None:
            len_y = len_x

        if len_x <= 0 or len_y <= 0:
            raise ValueError('len_x and len_y must be a positive numbers')

        self.len_x = len_x
        self.len_y = len_y

    @property
    def bounding_rectangle(self):
        br = BoundingRectangle(
            min_x=-self.len_x/2,
            max_x=self.len_x/2,
            min_y=-self.len_y/2,
            max_y=self.len_y/2,
        )
        return br

    def who_is_in(self, cell_centers):
        ni, nj, _ = cell_centers.shape
        isin = np.zeros((ni, nj), dtype=bool)
        br = self.bounding_rectangle
        for i, j in product(range(ni), range(nj)):
            [cx, cy] = cell_centers[i, j]
            isin[i, j] = cx >= br.min_x and \
                         cx <= br.max_x and \
                         cy >= br.min_y and \
                         cy <= br.max_y
        return isin
