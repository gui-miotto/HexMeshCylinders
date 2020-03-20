import matplotlib.pyplot as plt

from stack import Stack
from cylinder import Cylinder
from face import PatchSpec


edge = 0.5E-3

def get_odd_diam(float_num):
    int_num = int(round(float_num / edge))
    return int_num + 1 if int_num % 2 == 0 else int_num


Cylinder.edge = edge
cylinders = [
    Cylinder(diameter=get_odd_diam(10E-3), height=30E-3, n_layers=60)
]

s = Stack(cylinders, verbose=True)
s.name_patches([
        PatchSpec('bottom', 'wall', 0),
        PatchSpec('lateral', 'wall', 1),
        PatchSpec('top', 'patch', 2)
    ])
s.export('fake_case/constant/polyMesh_basic/')

