import math
import numpy as np

from HexMeshCylinders import Stack, PatchSpec
from HexMeshCylinders.Shapes import Circle


# Get the diameter of the hourglass as a function of the z-coordinate
def hour_glass_diam(z):
    return 2E-2 * (.2 + math.atan(z * 100) ** 2.)


edge = 1E-3  # 1 milimeter
layer_height = 2. * edge
stack = Stack(cell_edge=edge, verbose=True)

for z in np.arange(-4E-2, 4E-2, layer_height):
    stack.add_solid(
        shape2d=Circle(diameter=hour_glass_diam(z)),
        height=layer_height,
        n_layers=1
    )

stack.build_mesh()

# Patches can be grouped, be renamed and have their types altered
stack.name_patches([
    PatchSpec(name='bottom', type='wall', top_patch=0),
    PatchSpec(name='glass', type='wall', top_patch=stack.n_patches - 2),
    PatchSpec(name='top', type='patch', top_patch=stack.n_patches - 1)
])

stack.export('/tmp/HexMeshCylinders/hourglass')
