from itertools import product
from typing import List

from .cell_list import CellList
from .printer import Printer


class InternalFaceList():
    def __init__(self, isin, celllist: CellList, n_layers: List[int], verbose: bool):
        self.isin = isin
        self.celllist = celllist
        self._print = Printer(verbose)

        self.faces = list()

    def build_list(self):
        nx, ny, nz = self.isin.shape
        n_cells = self.isin.size
        all_faces = []
        for n, (i, j, k) in enumerate(product(range(nx), range(ny), range(nz))):
            if (n+1) % 10000 == 0:
                prog = n / n_cells * 100.
                self._print(f'Reached cell {n+1} of {n_cells} ({prog:.2f}%)')
            if self.isin[i, j, k]:
                cell_add = (i, j, k)
                all_faces.append(self.celllist.get_cell_face(cell_add, 'up'))
                all_faces.append(self.celllist.get_cell_face(cell_add, 'north'))
                all_faces.append(self.celllist.get_cell_face(cell_add, 'east'))

        self.faces = [face for face in all_faces if face.neighbour is not None]

    def __len__(self):
        return len(self.faces)
