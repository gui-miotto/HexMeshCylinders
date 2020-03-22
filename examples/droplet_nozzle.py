import math
from HexMeshCylinders import Cylinder, Stack, PatchSpec

edge = 5E-6  # 5 micro meters

Cylinder.cell_edge = edge
cylinders = [
    Cylinder(diameter=Cylinder.conv_diam(150E-6), height=300E-6, n_layers=60), #atmosphere
    Cylinder(diameter=Cylinder.conv_diam( 50E-6), height=150E-6, n_layers=30), #nozzle
    Cylinder(diameter=Cylinder.conv_diam(300E-6), height=200E-6, n_layers=40), #reservoir
    Cylinder(diameter=Cylinder.conv_diam(350E-6), height= 50E-6, n_layers= 3) #pres vessel
]

stack = Stack(cylinders, verbose=True)
stack.name_patches([
        PatchSpec('atmosphere', 'patch', 1),
        PatchSpec('nozzle_tip', 'wall', 2),
        PatchSpec('reservoir_nozzle', 'wall', 5),
        PatchSpec('pressure_vessel', 'wall', 7),
        PatchSpec('pressure_inlet', 'patch', 8)
    ])
stack.export('fake_case/constant/polyMesh/')
