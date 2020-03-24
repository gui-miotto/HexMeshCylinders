from HexMeshCylinders import Cylinder, Stack


# Cylinder.cell_edge defines the x and y dimensions for all the cells in the mesh
Cylinder.cell_edge = 1E-3  # 1 milimeter

# The volume will be made of two cylinders,
cylinders = [
    Cylinder(diameter=51, height=100E-3, n_layers=100),  # this one with 51 cells on its diameter,
    Cylinder(diameter=21, height= 50E-3, n_layers= 20),  # and this one with a diameter of 21 cells.
]

stack = Stack(cylinders, verbose=True)
stack.export('/tmp/HexMeshCylinders/basic')
