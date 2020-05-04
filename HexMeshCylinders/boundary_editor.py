from typing import List
from itertools import chain

from .boundary import Boundary
from .boundary_list import BoundaryList


class BoundaryEditor():
    def __init__(self, bound_list: BoundaryList):
        self.boundaries = bound_list

    def edit_boundary(self, index: int, new_name: str = None, new_btype: str = None):
        if new_name is not None:
            self.boundaries[index].name = new_name
        if new_btype is not None:
            self.boundaries[index].b_type = new_btype

    def merge_boundaries(self, indices: List[int], name: str = None, b_type: str = None):

        first_boundary = self.boundaries[indices[0]]
        name = first_boundary.name if name is None else name
        b_type = first_boundary.b_type if b_type is None else b_type

        selected_boundaries = [self.boundaries[i] for i in indices]
        faces = [face for face in chain.from_iterable(selected_boundaries)]

        self.boundaries.remove(indices)

        newBound = Boundary(name=name, faces=faces, b_type=b_type)
        self.boundaries.append(newBound)

        return len(self.boundaries)
