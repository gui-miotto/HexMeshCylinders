
import matplotlib.pyplot as plt

from stack import Stack
from cylinder import Cylinder

Cylinder.edge = .1
#cylinders = [
#    Cylinder(diameter=7, height=1., n_layers=2),
#    Cylinder(diameter=13, height=2., n_layers=3),
#]

cylinders = [
    Cylinder(diameter=5, height=.1, n_layers=1),
]


s = Stack(cylinders, verbose=True)
s.export('fake_case/constant/polyMesh/')


for n in range(1):
    plt.matshow(s.isin[:, :, n])
    plt.show()

