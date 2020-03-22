from itertools import product
import numpy as np

from .headers import point_header

class PointList():
    def __init__(self, isin, vertex):
        self.isin = isin
        self.vertex = vertex
        self._pointlist = self._build_list()  # list of vertex addresses (not space locations)
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
        points = np.ones(self.vertex.shape[:-1], dtype=np.int) * -1  #TODO: replace this by a sparse matrix
        for n, p in enumerate(self._pointlist):
            points[p] = n
        return points

    def __getitem__(self, key):
        return self._pointlist[key]

    def __len__(self):
        return len(self._pointlist)

    def index(self, i, j, k):
        return self._pointarray[(i, j, k)]

    def export(self, filepath):
        with open(filepath + 'points', 'w') as fw:
            fw.write(point_header)
            fw.write("\n")
            fw.write(str(len(self._pointlist)) + "\n")
            fw.write("(\n")
            for point_add in self._pointlist:
                location = self.vertex[point_add]
                fw.write(str(tuple(location)).replace(',', '') + "\n")
            fw.write(")\n")
            fw.write("\n")
