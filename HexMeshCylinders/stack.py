from pathlib import Path
from typing import List
import math


import numpy as np

from .Shapes.shape2D import Shape2D, BoundingRectangle


from .point import PointList
from .cell import CellList
from .face import FaceList, Patch, PatchSpec
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
            pointlist=self.pointlist,
            celllist=self.celllist,
            n_layers=self.n_layers,
            verbose=self.verbose,
            )

    @property
    def n_patches(self):
        """
        Number of patches
        """
        return len(self.facelist.patches)

    def name_patches(self, patch_specs: List[PatchSpec]):
        """Group patches, give them names and assing their types.

        Parameters
        ----------
        patch_specs : List[PatchSpec]
            A PatchSpec is a tupple containing (name, type, last_patch).
             * name is the patch name and can be anything e.g. nozzle
             * type is any valid OpenFoam boundary type, e.g wall
             * last_patch is the index of last layer that will compose the grouped patch.
               The patches between patch_specs[n-1][2] and patch_specs[n][2] will be
               lumped together into a single patch.
        """

        new_patches = []
        old_patches = self.facelist.patches
        if len(old_patches) - 1 != patch_specs[-1].top_patch:
            raise ValueError(f"The top_patch of the last patch should be {len(old_patches) - 1}")
        for i in range(len(patch_specs)-1):
            if patch_specs[i+1].top_patch <= patch_specs[i].top_patch:
                raise ValueError("Top patches should be ordered in ascending order")

        base_patch = 0
        for pspec in patch_specs:
            patches_to_merge = old_patches[base_patch:pspec.top_patch+1]
            startFace = patches_to_merge[0].startFace
            nFaces = sum([p.nFaces for p in patches_to_merge])
            newPatch = Patch(name=pspec.name, type=pspec.type, startFace=startFace, nFaces=nFaces)
            new_patches.append(newPatch)
            base_patch = pspec.top_patch + 1

        self.facelist.patches = new_patches

    def export(self, filepath):
        Path(filepath).mkdir(parents=True, exist_ok=True)
        self._print("Exporting point list")
        self.pointlist.export(filepath)
        self._print("Exporting face list")
        self.facelist.export(filepath)
        self._print("Done exporting")

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
