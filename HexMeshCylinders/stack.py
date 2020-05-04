from pathlib import Path
from typing import List
import math

import numpy as np

from .Shapes.shape2D import Shape2D, BoundingRectangle
from .point_list import PointList
from .cell_list import CellList
from .face_list import FaceList
from .boundary_editor import BoundaryEditor
from .printer import Printer


class Stack():
    def __init__(self, cell_edge: float, verbose: bool = False):
        """Specifies a volume that is made of a stack of solids

        Parameters
        ----------
        cell_edge : float
            Used as x and y dimensions for all cells of the mesh.
        verbose : bool, optional
            If True, outputs information about the progress of mesh construction, by default False.
        """

        self.edge = cell_edge
        self._print = Printer(verbose)
        self.verbose = verbose

        self.br = BoundingRectangle(0., 0., 0., 0.)
        self.z_cell_coords = [0.]
        self.shapes = []
        self.n_layers = []

    def add_solid(self, shape2d: Shape2D, height: float, n_layers: int = None):
        if n_layers is not None and not np.issubdtype(type(n_layers), np.integer):
            raise TypeError('n_layers must be an integer or None')
        if n_layers is None:
            n_layers = int(round(height / self.edge))

        self.shapes.append(shape2d)
        self.n_layers.append(n_layers)

        # Append new z_cell_coords
        current_top = self.z_cell_coords[-1]
        new_top = current_top + height
        vertical_spacing = np.linspace(current_top, new_top, n_layers + 1).tolist()
        self.z_cell_coords.extend(vertical_spacing[1:])

        # Adjust bounding rectangle
        sbr = shape2d.bounding_rectangle
        self.br = BoundingRectangle(
            min_x=min(self.br.min_x, sbr.min_x),
            max_x=max(self.br.max_x, sbr.max_x),
            min_y=min(self.br.min_y, sbr.min_y),
            max_y=max(self.br.max_y, sbr.max_y),
        )

    def build_mesh(self):
        self._print("Generating list of active cells")
        self.isin = self._who_is_in()
        self._print("Generating wireframe")
        self.vertex = self._build_vertex()
        self._print("Generating list of active points")
        self.pointlist = PointList(self.isin, self.vertex)
        self._print("Indexing active cells")
        self.celllist = CellList(self.isin, self.pointlist)
        self._print(f"Number of active cells{len(self.celllist)} of {self.isin.flatten().shape[0]}")
        self._print("Generating list of faces")
        self.facelist = FaceList(
            isin=self.isin,
            celllist=self.celllist,
            n_layers=self.n_layers,
            verbose=self.verbose,
            )

    def get_boundary_editor(self):
        return BoundaryEditor(bound_list=self.facelist.boundary_list)

    def export(self, filepath):
        Path(filepath).mkdir(parents=True, exist_ok=True)
        self._print("Exporting point list")
        self.pointlist.export(filepath)
        self._print("Exporting face list")
        self.facelist.export(filepath)
        self._print("Done exporting")


    @property
    def n_patches(self):
        """
        Number of patches
        """
        return self.facelist.n_boundaries

    def _who_is_in(self):
        # Create the horizontal grid
        x_cell_centers = self._get_vertical_cell_centers(self.br.min_x, self.br.max_x)
        y_cell_centers = self._get_vertical_cell_centers(self.br.min_y, self.br.max_y)
        cx, cy = np.meshgrid(x_cell_centers, y_cell_centers)
        centers_2D = np.array([cx, cy])
        centers_2D = np.swapaxes(centers_2D, 0, 2)

        total_n_layers = sum(self.n_layers)

        isin = np.zeros((centers_2D.shape[0], centers_2D.shape[1], total_n_layers), dtype=bool)
        k = 0
        for shape2d, n_layers in zip(self.shapes, self.n_layers):
            shape2d_isin = shape2d.who_is_in(centers_2D)
            isin[:, :, k:k+n_layers] = shape2d_isin[:, :, np.newaxis]
            k += n_layers

        return isin

    def _get_vertical_cell_centers(self, min_c, max_c):
        n_cells = math.ceil((max_c - min_c) / self.edge)
        half_spam = (n_cells - 1) * self.edge / 2.
        cell_coords = np.linspace(-half_spam, half_spam, n_cells)
        return cell_coords

    def _get_vertical_cell_coords(self, min_c, max_c):
        n_cells = math.ceil((max_c - min_c) / self.edge)
        half_spam = n_cells * self.edge / 2.
        cell_coords = np.linspace(-half_spam, half_spam, n_cells + 1)
        return cell_coords

    def _build_vertex(self):
        x_cell_coords = self._get_vertical_cell_coords(self.br.min_x, self.br.max_x)
        y_cell_coords = self._get_vertical_cell_coords(self.br.min_y, self.br.max_y)
        vx, vy, vz = np.meshgrid(x_cell_coords, y_cell_coords, self.z_cell_coords, indexing='ij')
        vertex = np.array([vx, vy, vz])
        vertex = np.moveaxis(vertex, 0, -1)
        return vertex
