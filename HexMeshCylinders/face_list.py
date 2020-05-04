from itertools import product
from collections import namedtuple
import os

from .internal_face_list import InternalFaceList
from .boundary_list import BoundaryList
from .printer import Printer
from .headers import faces_header, owner_header, neighbour_header, boundary_header


PatchSpec = namedtuple('PatchSpec', ['name', 'type', 'top_patch'])


class FaceList():
    def __init__(self, isin, celllist, n_layers, verbose):

        self.internal_faces = InternalFaceList(isin, celllist, n_layers, verbose)
        self.boundary_list = BoundaryList(isin, celllist, n_layers, verbose)
        self._print = Printer(verbose)

        self._build_list()

    def export(self, polyMesh_path):
        self._print("Exporting faces, owner and neighbour")
        self._export_faces(polyMesh_path=polyMesh_path)
        self._print("Exporting boundary")
        self.boundary_list.export(startFace=len(self.internal_faces), polyMesh_path=polyMesh_path)

    def _export_faces(self, polyMesh_path: str):
        all_faces = self.internal_faces.faces + self.boundary_list.faces
        n_faces = len(all_faces)

        faces_filepath = os.path.join(polyMesh_path, 'faces')
        f_faces = open(faces_filepath, 'w')
        f_faces.write(faces_header + '\n')
        f_faces.write(str(n_faces) + '\n')
        f_faces.write('(\n')

        owner_filepath = os.path.join(polyMesh_path, 'owner')
        f_owner = open(owner_filepath, 'w')
        f_owner.write(owner_header + '\n')
        f_owner.write(str(n_faces) + '\n')
        f_owner.write('(\n')

        neigh_filepath = os.path.join(polyMesh_path, 'neighbour')
        f_neigh = open(neigh_filepath, 'w')
        f_neigh.write(neighbour_header + '\n')
        f_neigh.write(str(len(self.internal_faces)) + '\n')
        f_neigh.write('(\n')

        for face in all_faces:
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

    def _build_list(self):
        self._print("Generating list of internal faces")
        self.internal_faces.build_list()
        self._print("Generating list of boundary faces")
        self.boundary_list.build_list()



