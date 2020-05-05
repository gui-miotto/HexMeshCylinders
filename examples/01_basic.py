from HexMeshCylinders import Stack
from HexMeshCylinders.Shapes import Rectangle, Circle

# All cells in this mesh will have x and y edges of 1.5cm.
stack = Stack(cell_edge=.015, verbose=True)

# The bottom most solid is a rectangle with height 1m. This height will be slipt into
# 20 layers. So cells in this solid will have z edges of 5 cm
stack.add_solid(
    shape2d=Rectangle(len_x=.8, len_y=1.2),
    height=1.,
    n_layers=20,
)

# On top of the rectangle, we add a circle with height 80 cm.
# Because n_layers was not specified, it will be calculated in such a way that the z edges are
# as close as possible to the x and y edges. In other words, cells of this solid will be as similar
# as possible to cubes.
stack.add_solid(
    shape2d=Circle(diameter=.6),
    height=.8,
)

# Creates and exports the mesh
stack.build_mesh()
stack.export('/tmp/HexMeshCylinders/basic')
