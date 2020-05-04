import math
import numpy as np

from HexMeshCylinders import Stack
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
be = stack.get_boundary_editor()
be.edit_boundary(index=0, new_name='bottom', new_btype='wall')
be.edit_boundary(index=stack.n_patches - 1, new_name='top', new_btype='patch')
be.merge_boundaries(
    indices=list(range(1, stack.n_patches - 1)),
    name='glass',
    b_type='wall',
)

stack.export('/tmp/HexMeshCylinders/hourglass')
