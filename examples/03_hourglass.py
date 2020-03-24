import math
import numpy as np
from HexMeshCylinders import Cylinder, Stack, PatchSpec

edge = 1E-3  # 1 milimeter
Cylinder.cell_edge =  edge

# Get the diameter of the hourglass as a function of the z-coordinate
hour_glass_diam = lambda z : 2E-2 * (.2 + math.atan(z * 100) ** 2.)

cylinders = list()
layer_height = 2. * edge
for z in np.arange(-4E-2, 4E-2, layer_height):
    new_cyl_diam = Cylinder.conv_diam(hour_glass_diam(z))
    new_cyl = Cylinder(diameter=new_cyl_diam, height=layer_height, n_layers=1)
    cylinders.append(new_cyl)


stack = Stack(cylinders, verbose=True)
stack.name_patches([
    PatchSpec('bottom', 'wall', 0),
    PatchSpec('glass', 'wall', stack.n_patches - 2),
    PatchSpec('top', 'patch', stack.n_patches - 1)
])

stack.export('/tmp/HexMeshCylinders/hourglass')
