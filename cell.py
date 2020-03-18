from itertools import product
import numpy as np

from face import Face

class CellList():
    def __init__(self, isin, pointlist):
        self.isin = isin
        self.pointlist = pointlist
        self._celllist = self._build_list()

    def get_cell_face(self, cell_address, direction):
        i, j, k = cell_address
        cell_from = np.array(cell_address)
        cell_from_index = self.index(cell_address)
        # We first assume that cell_to has a larger index than cell_from
        if direction == "up":
            cell_to = cell_from + [0, 0, 1]
            vertex = (
                self.pointlist.index(i,     j,     k + 1),
                self.pointlist.index(i + 1, j,     k + 1),
                self.pointlist.index(i + 1, j + 1, k + 1),
                self.pointlist.index(i,     j + 1, k + 1))
        elif direction == "down":
            cell_to = cell_from + [0, 0, -1]
            vertex = (
                self.pointlist.index(i,     j,     k),
                self.pointlist.index(i,     j + 1, k),
                self.pointlist.index(i + 1, j + 1, k),
                self.pointlist.index(i + 1, j,     k))
        elif direction == "west":
            cell_to = cell_from + [-1, 0, 0]
            vertex = (
                self.pointlist.index(i, j,     k    ),
                self.pointlist.index(i, j,     k + 1),
                self.pointlist.index(i, j + 1, k + 1),
                self.pointlist.index(i, j + 1, k    ))
        elif direction == "east":
            cell_to = cell_from + [1, 0, 0]
            vertex = (
                self.pointlist.index(i + 1, j,     k    ),
                self.pointlist.index(i + 1, j + 1, k    ),
                self.pointlist.index(i + 1, j + 1, k + 1),
                self.pointlist.index(i + 1, j,     k + 1))
        elif direction == "north":
            cell_to = cell_from + [0, 1, 0]
            vertex = (
                self.pointlist.index(i,     j + 1, k    ),
                self.pointlist.index(i,     j + 1, k + 1),
                self.pointlist.index(i + 1, j + 1, k + 1),
                self.pointlist.index(i + 1, j + 1, k    ))
        elif direction == "south":
            cell_to = cell_from + [0, -1, 0]
            vertex = (
                self.pointlist.index(i,     j, k    ),
                self.pointlist.index(i + 1, j, k    ),
                self.pointlist.index(i + 1, j, k + 1),
                self.pointlist.index(i,     j, k + 1))
        else:
            raise ValueError('Invalid direction')

        cell_to = tuple(cell_to)
        if self._is_cell_address_out_of_bounds(cell_to) or not self.isin[cell_to]:
            # This means we the face is a boundary
            return Face(vertex, cell_from_index)
        else:
            cell_to_index = self.index(cell_to)
            if cell_from_index > cell_to_index:
                return Face(vertex[::-1], cell_to_index, cell_from_index)
            else:
                return Face(vertex, cell_from_index, cell_to_index)

    def _is_cell_address_out_of_bounds(self, address):
        for ind, add_coord in enumerate(address):
            if add_coord < 0 or add_coord >= self.isin.shape[ind]:
                return True
        return False

    def _build_list(self):
        nx, ny, nz = self.isin.shape
        celllist = []
        for i, j, k in product(range(nx), range(ny), range(nz)):
            if self.isin[i, j, k]:
                celllist.append((i, j, k))
        return celllist

    def __getitem__(self, key):
        return self._celllist[key]

    def __len__(self):
        return len(self._celllist)

    def index(self, key):
        return self._celllist.index(key)

