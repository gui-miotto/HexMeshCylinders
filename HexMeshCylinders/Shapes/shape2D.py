from collections import namedtuple
from abc import ABC, abstractmethod

BoundingRectangle = namedtuple('BoundingRectangle', ['min_x', 'max_x', 'min_y', 'max_y'])

class Shape2D():

    def __init__(self):
        pass

    @property
    @abstractmethod
    def bounding_rectangle(self):
        raise NotImplementedError

    @abstractmethod
    def who_is_in(self, cell_centers):
        raise NotImplementedError
