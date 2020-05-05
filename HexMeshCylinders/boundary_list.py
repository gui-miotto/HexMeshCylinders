from itertools import product, chain
from typing import List
import os

from .boundary import Boundary
from .printer import Printer
from .headers import boundary_header


class BoundaryList():
    def __init__(self, isin, celllist, n_layers, verbose):
        self.isin = isin
        self.celllist = celllist
        self.n_layers = n_layers
        self._print = Printer(verbose)

        self.boundaries = list()

    def __getitem__(self, key):
        return self.boundaries[key]

    def __len__(self):
        return len(self.boundaries)

    def append(self, boundary: Boundary):
        self.boundaries.append(boundary)

    def remove(self, indices: List[int]):
        tmp_list = [i for j, i in enumerate(self.boundaries) if j not in indices]
        self.boundaries = tmp_list

    @property
    def faces(self):
        """ A list with all faces of all boundaries """
        return [face for face in chain.from_iterable(self.boundaries)]

    def export(self, startFace: int, polyMesh_path: str):
        self._print("Exporting boundary")
        bound_filepath = os.path.join(polyMesh_path, 'boundary')
        with open(bound_filepath, 'w') as fw:
            fw.write(boundary_header + '\n')
            fw.write(str(len(self.boundaries)) + "\n")
            fw.write("(\n")
            for pid, bound in enumerate(self.boundaries):
                fw.write(bound.name + "\n")
                fw.write("\t{\n")
                fw.write("\t\ttype       " + bound.b_type + ";\n")
                fw.write("\t\tnFaces     " + str(len(bound)) + ";\n")
                fw.write("\t\tstartFace  " + str(startFace) + ";\n")
                fw.write("\t}\n")
                startFace += len(bound)
            fw.write(")\n")

    def build_list(self):
        # bottom most boundary
        self._print("Generating bottom most boundary")
        self._get_boundary_horizontal(0)

        # intermediate boundaries
        n_solids = len(self.n_layers)
        l0 = 0

        for solid_id, nl in enumerate(self.n_layers):
            self._print(f"Generating boundaries for solid {solid_id+1} of {n_solids}")
            l1 = l0 + nl
            self._get_boundary_vertical(l0, l1)
            self._get_boundary_horizontal(l1)
            l0 = l1

    def _get_boundary_horizontal(self, layer):
        """ Addes one horizontal boundary along a specified layer """
        nx, ny, nz = self.isin.shape
        k = layer
        faces = list()
        for i, j in product(range(nx), range(ny)):
            if k > 0 and self.isin[i, j, k - 1]:
                if k == nz or not self.isin[i, j, k]:
                    cell_add = (i, j, k - 1)
                    face = self.celllist.get_cell_face(cell_add, 'up')
                    assert face.neighbour is None
                    faces.append(face)
            if k < nz and self.isin[i, j, k]:
                if k == 0 or not self.isin[i, j, k - 1]:
                    cell_add = (i, j, k)
                    face = self.celllist.get_cell_face(cell_add, 'down')
                    assert face.neighbour is None
                    faces.append(face)
        new_bound = Boundary(
            name='boundary_' + str(len(self.boundaries)),
            faces=faces,
        )
        self.boundaries.append(new_bound)

    def _get_boundary_vertical(self, layer_start, layer_end):
        """ Addes one vertical boundary along a specified range of layers """
        assert layer_end >= layer_start
        nx, ny, _ = self.isin.shape
        k0 = layer_start
        layers = list(range(layer_start, layer_end))
        faces = list()
        for i, j in product(range(nx), range(ny)):
            if self.isin[i, j, k0]:
                # For each of the four directions, check if cell is at the edge
                # of the grid or if it has no neighbour
                boundary_directions = []
                if j == ny - 1 or not self.isin[i, j + 1, k0]:
                    boundary_directions.append('north')
                if i == nx - 1 or not self.isin[i + 1, j, k0]:
                    boundary_directions.append('east')
                if j == 0 or not self.isin[i, j - 1, k0]:
                    boundary_directions.append('south')
                if i == 0 or not self.isin[i - 1, j, k0]:
                    boundary_directions.append('west')
                for bd in boundary_directions:
                    for k in layers:
                        cell_add = (i, j, k)
                        face = self.celllist.get_cell_face(cell_add, bd)
                        faces.append(face)
        new_bound = Boundary(
            name='boundary_' + str(len(self.boundaries)),
            faces=faces,
        )
        self.boundaries.append(new_bound)
