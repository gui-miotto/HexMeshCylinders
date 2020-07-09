from typing import List, Tuple
from itertools import chain
import math

import numpy as np

from .boundary import Boundary
from .boundary_list import BoundaryList


def atan(x, y, set_zero_to=None):
    if x == 0:
        angle = math.pi / 2. if y > 0 else 3. * math.pi / 2.
    else:
        angle = math.atan(y / x)
        if x > 0:
            angle = angle if y >= 0 else angle + 2 * math.pi
        else:
            angle += math.pi

    if set_zero_to is not None:
        angle -= set_zero_to
        angle = angle if angle >= 0. else 2. * math.pi + angle

    return angle


class BoundaryEditor():
    def __init__(self, bound_list: BoundaryList, point_list):
        self.boundaries = bound_list
        self.points = point_list

    @property
    def n_boundaries(self):
        return len(self.boundaries)

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

        # Remove old smaller boundaries and add new big boundary
        self.boundaries.remove(indices)
        newBound = Boundary(name=name, faces=faces, b_type=b_type)
        self.boundaries.append(newBound)

    def _get_face_centers(self, bound_index):
        bound = self.boundaries[bound_index]
        faces_center = list()
        for face in bound.faces:
            vertex_grid_addresses = [self.points[v] for v in face.vertex]
            vertex_coords = [self.points.vertex[v] for v in vertex_grid_addresses]
            faces_center.append(np.mean(vertex_coords, axis=0))
        return faces_center

    def split_boundary_coord(self,
                             index: int,
                             coord_name: str,
                             coord_value: float,
                             new_names: Tuple[str, str] = None,
                             new_types: Tuple[str, str] = None,
                             ):
        fcenters = self._get_face_centers(bound_index=index)
        bound = self.boundaries[index]
        sel_coord = ['x', 'y', 'z'].index(coord_name)

        # Split faces according to the selected coordinate
        new_faces = ([], [])
        for face, center in zip(bound.faces, fcenters):
            if(center[sel_coord] > coord_value):
                new_faces[0].append(face)
            else:
                new_faces[1].append(face)

        # Adjust names and types
        if new_names is None:
            new_names = (bound.name + "_more", bound.name + "_less")
        if new_types is None:
            new_types = (bound.b_type, bound.b_type)

        # Remove old large boundary and add the two new smaller boundaries
        self.boundaries.remove([index])
        for i in range(2):
            new_bound = Boundary(
                name=new_names[i],
                faces=new_faces[i],
                b_type=new_types[i],
            )
            self.boundaries.append(new_bound)

    def split_boundary_pizza(self,
                             index: int,
                             angles: List[float],
                             new_names: List[str] = None,
                             new_types: List[str] = None,
                             ):
        # Input validation
        if min(angles) < 0 or max(angles) > 2. * math.pi:
            raise ValueError('Angles should be in the range from 0. to 2.*pi')
        n_angles = len(angles)
        if n_angles < 2:
            raise ValueError('At least two angles must be provided')
        if new_names is not None and n_angles != len(new_names):
            raise ValueError(str(n_angles) + 'names should be provided')
        if new_types is not None and n_angles != len(new_types):
            raise ValueError(str(n_angles) + 'b_types should be provided')

        # Adjust names and types
        bound = self.boundaries[index]
        if new_names is None:
            new_names = [bound.name + '_' + str(i) for i in range(n_angles)]
        if new_types is None:
            new_types = [bound.b_type] * n_angles

        # Split faces according to their angle value
        angles = sorted(angles)
        angles_low = np.array(angles) - angles[0]
        angles_high = np.hstack((angles_low[1:], [2. * math.pi]))

        new_faces = [list() for _ in range(n_angles)]
        fcenters = self._get_face_centers(bound_index=index)

        for face, center in zip(bound.faces, fcenters):
            face_angle = atan(x=center[0], y=center[1], set_zero_to=angles[0])
            for face_id, (ang_min, ang_max) in enumerate(zip(angles_low, angles_high)):
                if face_angle >= ang_min and face_angle < ang_max:
                    new_faces[face_id].append(face)
                    break

        # Remove old large boundary and add the new smaller boundaries
        self.boundaries.remove([index])
        for i in range(n_angles):
            new_bound = Boundary(
                name=new_names[i],
                faces=new_faces[i],
                b_type=new_types[i],
            )
            self.boundaries.append(new_bound)

    def split_boundary_rings(self,
                             index: int,
                             radi: List[float],
                             new_names: List[str] = None,
                             new_types: List[str] = None,
                             ):
        # Input validation
        n_radi = len(radi)
        n_new_bounds = n_radi + 1
        if n_radi < 1:
            raise ValueError('At least one radius must be provided')
        if new_names is not None and n_new_bounds != len(new_names):
            raise ValueError(str(n_new_bounds) + 'names should be provided')
        if new_types is not None and n_new_bounds != len(new_types):
            raise ValueError(str(n_new_bounds) + 'b_types should be provided')

        # Adjust names and types
        bound = self.boundaries[index]
        if new_names is None:
            new_names = [bound.name + '_' + str(i) for i in range(n_new_bounds)]
        if new_types is None:
            new_types = [bound.b_type] * n_radi

        # Split faces according to their angle value
        radi = sorted(radi)
        new_faces = [list() for _ in range(n_new_bounds)]
        fcenters = self._get_face_centers(bound_index=index)

        for face, center in zip(bound.faces, fcenters):
            face_dist = math.sqrt(center[0] ** 2. + center[1] ** 2.)
            face_allocated = False
            for new_bound_id, ring_radius in enumerate(radi):
                if ring_radius >= face_dist:
                    new_faces[new_bound_id].append(face)
                    face_allocated = True
                    break
            if not face_allocated:
                new_faces[-1].append(face)

        # Remove old large boundary and add the new smaller boundaries
        self.boundaries.remove([index])
        for i in range(n_new_bounds):
            new_bound = Boundary(
                name=new_names[i],
                faces=new_faces[i],
                b_type=new_types[i],
            )
            self.boundaries.append(new_bound)
