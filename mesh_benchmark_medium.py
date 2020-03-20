import matplotlib.pyplot as plt

from stack import Stack
from cylinder import Cylinder
from face import PatchSpec


edge = 2E-6

def get_odd_diam(float_num):
    int_num = int(round(float_num / edge))
    return int_num + 1 if int_num % 2 == 0 else int_num


Cylinder.edge = edge
cylinders = [
    Cylinder(diameter=get_odd_diam(350E-6), height= 50E-6, n_layers=  5),
    Cylinder(diameter=get_odd_diam(300E-6), height=200E-6, n_layers= 25),
    Cylinder(diameter=get_odd_diam( 50E-6), height=150E-6, n_layers= 75),
    Cylinder(diameter=get_odd_diam(150E-6), height=200E-6, n_layers=100)
]

s = Stack(cylinders, verbose=True)
s.name_patches([
        PatchSpec('bottom', 'wall', 0),
        PatchSpec('atmosphere', 'patch', 1),
        PatchSpec('nozzle_tip', 'wall', 2),
        PatchSpec('reservoir_nozzle', 'wall', 5),
        PatchSpec('pressure_vessel', 'wall', 7),
        PatchSpec('pressure_inlet', 'patch', 8)
    ])
s.export('fake_case/constant/polyMesh/')

