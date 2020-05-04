from typing import List, Tuple
from itertools import chain

import numpy as np

from .boundary import Boundary
from .boundary_list import BoundaryList


class BoundaryEditor():
    def __init__(self, bound_list: BoundaryList, point_list):
        self.boundaries = bound_list
        self.points = point_list

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

    def split_boundaries_coord(self,
                               index: int,
                               coord_name: str,
                               coord_value: float,
                               new_names: Tuple[str, str] = None,
                               new_types: Tuple[str, str] = None,
                               ):
        bound = self.boundaries[index]
        sel_coord = ['x', 'y', 'z'].index(coord_name)

        new_faces = ([], [])
        for face in bound.faces:
            vertex_grid_addresses = [self.points[v] for v in face.vertex]
            vertex_coords = [self.points.vertex[v] for v in vertex_grid_addresses]
            face_center = np.mean(vertex_coords, axis=0)

            if(face_center[sel_coord] > coord_value):
                new_faces[0].append(face)
            else:
                new_faces[1].append(face)

        if new_names is None:
            new_names = (bound.name + "_a", bound.name + "_b")

        if new_types is None:
            new_types = (bound.b_type, bound.b_type)

        self.boundaries.remove([index])

        for i in range(2):
            new_bound = Boundary(
                name=new_names[i],
                faces=new_faces[i],
                b_type=new_types[i],
            )
            self.boundaries.append(new_bound)

        n_bounds = len(self.boundaries)

        return (n_bounds - 1, n_bounds)
