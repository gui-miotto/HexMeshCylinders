from itertools import product
from collections import namedtuple
import multiprocessing, time
import numpy as np

from .printer import Printer
from .headers import faces_header, owner_header, neighbour_header, boundary_header

Patch = namedtuple('Patch', ['name', 'type', 'startFace', 'nFaces'])
PatchSpec = namedtuple('PatchSpec', ['name', 'type', 'top_patch'])

class Face():
    def __init__(self, vertex, owner, neighbour=None):
        self.vertex = vertex
        self.owner = owner
        self.neighbour = neighbour


class FaceList():
    def __init__(self, isin, pointlist, celllist, cylinders, verbose):
        self.isin = isin
        self.pointlist = pointlist
        self.celllist = celllist
        self.cylinders = cylinders
        self._print = Printer(verbose)

        self._facelist = []
        self.patches = []
        self._build_list()

    def export(self, filepath):
        self._print("Exporting faces, owner and neighbour")
        self._export_faces(filepath)
        self._print("Exporting boundary")
        self._export_boundaries(filepath)

    def _num_internal_faces(self):
        n = 0
        for f in self._facelist:
            if f.neighbour is not None:
                n += 1
        return n

    def _export_faces(self, filepath):
        n_faces = len(self._facelist)

        f_faces = open(filepath + 'faces', 'w')
        f_faces.write(faces_header + '\n')
        f_faces.write(str(n_faces) + '\n')
        f_faces.write('(\n')

        f_owner = open(filepath + 'owner', 'w')
        f_owner.write(owner_header + '\n')
        f_owner.write(str(n_faces) + '\n')
        f_owner.write('(\n')

        f_neigh = open(filepath + 'neighbour', 'w')
        f_neigh.write(neighbour_header + '\n')
        f_neigh.write(str(self._num_internal_faces()) + '\n')
        f_neigh.write('(\n')

        for face in self._facelist:
            f_faces.write('4' + str(face.vertex).replace(',', '') + '\n')
            f_owner.write(str(face.owner) + '\n')
            if face.neighbour is not None:
                f_neigh.write(str(face.neighbour) + '\n')

        f_faces.write(')\n')
        f_owner.write(')\n')
        f_neigh.write(')\n')

        f_faces.close()
        f_owner.close()
        f_neigh.close()

    def _export_boundaries(self, filepath):
        with open(filepath + 'boundary', 'w') as fw:
            fw.write(boundary_header + '\n')
            fw.write(str(len(self.patches)) + "\n")
            fw.write("(\n")
            for pid, patch in enumerate(self.patches):
                fw.write(patch.name + "\n")
                fw.write("\t{\n")
                fw.write("\t\ttype       " + patch.type + ";\n")
                fw.write("\t\tnFaces     " + str(patch.nFaces)+ ";\n")
                fw.write("\t\tstartFace  " + str(patch.startFace)+ ";\n")
                fw.write("\t}\n")
            fw.write(")\n")

    def _build_list(self):
        self._print("Generating list of internal faces")
        self._get_internal_faces()
        self._print("Generating list of boundary faces")
        self._get_boundary_faces()

    def _get_internal_faces(self):
        nx, ny, nz = self.isin.shape
        n_cells = self.isin.size
        all_faces = []
        for n, (i, j, k) in enumerate(product(range(nx), range(ny), range(nz))):
            if (n+1) % 1000 == 0:
                prog = n / n_cells * 100.
                self._print(f'Reached cell {n+1} of {n_cells} ({prog:.2f}%)')
            if self.isin[i, j, k]:
                cell_add = (i, j, k)
                all_faces.append(self.celllist.get_cell_face(cell_add, 'up'))
                all_faces.append(self.celllist.get_cell_face(cell_add, 'north'))
                all_faces.append(self.celllist.get_cell_face(cell_add, 'east'))

        self._print("Removing boundaries from internal faces")
        internal_faces = [face for face in all_faces if face.neighbour is not None]
        self._facelist.extend(internal_faces)

    def _get_boundary_faces(self):
        # bottom most boundary
        self._print("Generating bottom most boundary")
        self._get_boundary_horizontal(0, 'down')

        # intermediate boundaries
        n_cyls = len(self.cylinders)
        l0 = 0
        for cyl in range(n_cyls):
            self._print(f"Generating boundaries for cylinder {cyl+1} of {n_cyls}")
            l1 = l0 + self.cylinders[cyl].n_layers
            layers = list(range(l0, l1))
            self._get_boundary_vertical(layers)
            l0 = l1

            if cyl < n_cyls - 1:
                if self.cylinders[cyl].diam > self.cylinders[cyl + 1].diam:
                    self._get_boundary_horizontal(l1 - 1, 'up')
                else:
                    self._get_boundary_horizontal(l1, 'down')

        # top most boundary
        self._print("Generating top most boundary")
        self._get_boundary_horizontal(l1 - 1, 'up')

    def _get_boundary_horizontal(self, layer, direction):
        assert direction in ['up', 'down']
        startFace = len(self._facelist)
        nFaces = 0
        nx, ny, nz = self.isin.shape
        k = layer
        for i, j in product(range(nx), range(ny)):
            if self.isin[i, j, k]:
                cell_add = (i, j, k)
                # For each of the four directions, check if cell is at the edge
                # of the grid or if it has no neighbour
                if direction=='up' and (k == nz - 1 or not self.isin[i, j, k + 1]):
                    face = self.celllist.get_cell_face(cell_add, 'up')
                    self._facelist.append(face)
                    nFaces += 1
                if direction=='down' and (k == 0 or not self.isin[i, j, k - 1]):
                    face = self.celllist.get_cell_face(cell_add, 'down')
                    self._facelist.append(face)
                    nFaces += 1
        newPatch = Patch(name='patch_' + str(len(self.patches)), type='patch',
            startFace=startFace, nFaces=nFaces)
        self.patches.append(newPatch)

    def _get_boundary_vertical(self, layers):
        startFace = len(self._facelist)
        nFaces = 0
        nx, ny, _ = self.isin.shape
        k0 = layers[0]
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
                        self._facelist.append(face)
                        nFaces += 1
        newPatch = Patch(name='patch_' + str(len(self.patches)), type='patch',
            startFace=startFace, nFaces=nFaces)
        self.patches.append(newPatch)
