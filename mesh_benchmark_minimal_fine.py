import matplotlib.pyplot as plt

from stack import Stack
from cylinder import Cylinder
from face import PatchSpec


edge = 1E-6

def get_odd_diam(float_num):
    int_num = int(round(float_num / edge))
    return int_num + 1 if int_num % 2 == 0 else int_num


Cylinder.edge = edge
cylinders = [
    Cylinder(diameter=get_odd_diam( 50E-6), height=100E-6, n_layers=100),
    Cylinder(diameter=get_odd_diam(150E-6), height=200E-6, n_layers=200)
]

s = Stack(cylinders, verbose=True)
s.name_patches([
        PatchSpec('bottom', 'wall', 0),
        PatchSpec('atmosphere', 'patch', 1),
        PatchSpec('nozzle_tip', 'wall', 2),
        PatchSpec('nozzle', 'wall', 3),
        PatchSpec('pressure_inlet', 'patch',4)
    ])
s.export('fake_case/constant/polyMesh_minimal_fine/')

