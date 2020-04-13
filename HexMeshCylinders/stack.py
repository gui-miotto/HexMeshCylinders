from pathlib import Path
from typing import List
import numpy as np

from .cylinder import Cylinder
from .point import PointList
from .cell import CellList
from .face import FaceList, Patch, PatchSpec
from .printer import Printer


class Stack():
    def __init__(self, cylinders: List[Cylinder], verbose=False):
        """Specifies a volume that is made of a stack of cylinders

        Parameters
        ----------
        cylinders : List[Cylinder]
            A list of cylinders to stack. cylinders[0] is the bottom most cylinder, and
             cylinders[-1] is the top most
        verbose : bool, optional
            Print runtimet messages, by default False
        """

        self.edge = Cylinder.cell_edge
        self.cylinders = cylinders
        self._print = Printer(verbose)

        self.max_diam = max([c.diameter for c in self.cylinders])

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
        self.facelist = FaceList(self.isin, self.pointlist, self.celllist, self.cylinders, verbose)

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
