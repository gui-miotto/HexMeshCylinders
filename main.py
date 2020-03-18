
import matplotlib.pyplot as plt

from stack import Stack
from cylinder import Cylinder
from face import PatchSpec

Cylinder.edge = .1

cylinders = [
    Cylinder(diameter=3, height=.1, n_layers=1),
    Cylinder(diameter=5, height=.1, n_layers=1),
]

"""
cylinders = [
    Cylinder(diameter=31, height=1.5, n_layers=10),
    Cylinder(diameter=13, height=1, n_layers=8),
]
"""

s = Stack(cylinders, verbose=True)
s.name_patches([
        #PatchSpec('A', 'wall', 0),
        PatchSpec('B', 'patch', 2),
        PatchSpec('C', 'wall', 4)
    ])


s.export('fake_case/constant/polyMesh/')



"""for n in range(1):
    plt.matshow(s.isin[:, :, n])
    plt.show()
"""
