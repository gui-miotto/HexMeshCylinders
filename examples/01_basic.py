from HexMeshCylinders import Stack
from HexMeshCylinders.Shapes import Rectangle, Circle

# All cells in this mesh will have x and y edges of 2cm.
stack = Stack(cell_edge=.02, verbose=True)

# The bottom most solid is a rectangle with height 50cm. This height will be slipt into
# 10 layers. So cells in this solid will have z edges of 5 cm
stack.add_solid(
    shape2d=Rectangle(len_x=1., len_y=.3),
    height=.5,
    n_layers=10,
)

# On top of the rectangle, we add a circle with height 6 cm.
# Because n_layers was not specified, it will be calculated in such a way that the z edges are
# as close as possible to the x and y edges. In other words, cells of this solid will be as similar
# as possible to cubes.
stack.add_solid(
    shape2d=Circle(diameter=.6),
    height=3.,
)

# Creates and exports the mesh
stack.build_mesh()
stack.export('/tmp/HexMeshCylinders/basic')
