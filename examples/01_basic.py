import math
from HexMeshCylinders import Cylinder, Stack, PatchSpec


Cylinder.cell_edge = 1E-3  # 1 milimeter

cylinders = [
    Cylinder(diameter=51, height=100E-3, n_layers=100),
    Cylinder(diameter=21, height= 50E-3, n_layers= 20),
]

stack = Stack(cylinders, verbose=True)
stack.export('/tmp/HexMeshCylinders/basic')
