import os
from itertools import product
import numpy as np

from .headers import point_header


class PointList():
    def __init__(self, isin: 'np.ndarray[bool]', vertex: 'np.ndarray[float]'):
        """[summary]

        Parameters
        ----------
        isin : np.ndarray[bool]
            Indicates which cells are active. shape=(i, j, k)
        vertex : np.ndarray[float]
            Phisical coordinates (x, y, z) of each grid vertex (i, j, k). shape=(i+1, j+1, k+1, 3)
        """
        self.isin = isin
        self.vertex = vertex

        # _pointlist is a linear list (with n entries) of grid addresses (i, j, k).
        # Not physical coordinates. shape=(n, 3).
        self._pointlist = self._build_list()
        # _pointarray  stores the index of inside _pointlist of each grid address.
        # This array just exist for performance reasons. shape=(i+1, j+1, k+1)
        self._pointarray = self._build_array()

    def _build_list(self):
        points = set()
        inc = [0, 1]
        nx, ny, nz = self.isin.shape
        for i, j, k in product(range(nx), range(ny), range(nz)):
            if self.isin[i, j, k]:
                for inc_x, inc_y, inc_z in product(inc, inc, inc):
                    new_address = (
                        i + inc_x,
                        j + inc_y,
                        k + inc_z)
                    points.add(new_address)
        return list(points)

    def _build_array(self):
        points = np.ones(self.vertex.shape[:-1], dtype=np.int) * -1  # TODO: replace by sparse ?
        for n, p in enumerate(self._pointlist):
            points[p] = n
        return points

    def __getitem__(self, key):
        return self._pointlist[key]

    def __len__(self):
        return len(self._pointlist)

    def index(self, i, j, k):
        return self._pointarray[(i, j, k)]

    def export(self, polyMesh_path):
        filepath = os.path.join(polyMesh_path, 'points')
        with open(filepath, 'w') as fw:
            fw.write(point_header)
            fw.write("\n")
            fw.write(str(len(self._pointlist)) + "\n")
            fw.write("(\n")
            for point_add in self._pointlist:
                location = self.vertex[point_add]
                fw.write(str(tuple(location)).replace(',', '') + "\n")
            fw.write(")\n")
            fw.write("\n")
