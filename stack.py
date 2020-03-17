from itertools import product
import numpy as np

from cylinder import Cylinder
from point import PointList
from cell import CellList
from face import FaceList

class Stack():
    def __init__(self, cylinders, verbose=False):
        self.edge = Cylinder.edge
        self.cylinders = cylinders
        self.verbose = verbose

        self.max_diam = max([c.diam for c in self.cylinders])

        self._print("Deactivating cells outside the volume")
        self.isin = self._who_is_in()
        self._print("Generating wireframe")
        self.vertex = self._build_vertex()
        self._print("Generating list of active points")
        self.pointlist = PointList(self.isin, self.vertex)
        self._print("Generating list of active cells")
        self.celllist = CellList(self.isin, self.pointlist)
        self._print("Generating list of faces")
        self.facelist = FaceList(self.isin, self.pointlist, self.celllist, self.cylinders, verbose)

    def export(self, filepath):
        self.pointlist.export(filepath)
        self.facelist.export(filepath)

    def _who_is_in(self):
        h_max = (self.max_diam - 1) * self.edge / 2.
        h_min = -h_max
        horiz_spacing = np.linspace(h_min, h_max, self.max_diam)

        cx, cy = np.meshgrid(horiz_spacing, horiz_spacing)
        centers_2D = np.array([cx, cy])
        centers_2D = np.moveaxis(centers_2D, 0, -1)

        n_layers = sum([c.n_layers for c in self.cylinders])

        isin = np.zeros((self.max_diam, self.max_diam, n_layers), dtype=bool)
        k = 0
        for c in self.cylinders:
            c_isin = c.who_is_in(centers_2D)
            isin[:, :, k:k+c.n_layers] = c_isin[:, :, np.newaxis]
            k += c.n_layers

        return isin

    def _build_vertex(self):
        h_max = self.max_diam * self.edge / 2.
        h_min = -h_max
        horiz_spacing = np.linspace(h_min, h_max, self.max_diam + 1)

        vert_spacing = np.array([])
        height_shift = 0
        for c in self.cylinders:
            cyl_vert_spa = c.vertical_spacing[:-1] + height_shift
            vert_spacing = np.hstack((vert_spacing, cyl_vert_spa))
            height_shift += c.height
        vert_spacing = np.hstack((vert_spacing, height_shift))

        vx, vy, vz = np.meshgrid(horiz_spacing, horiz_spacing, vert_spacing, indexing='ij')
        vertex = np.array([vx, vy, vz])
        vertex = np.moveaxis(vertex, 0, -1)

        return vertex

    def _print(self, text):
        if self.verbose:
            print(text)

