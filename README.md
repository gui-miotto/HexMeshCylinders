<p align="center">
  <img src="media/hexmeshcyl.png" alt="hexmeshcyl" width="500"/>
</p>

<!--# HexMeshCylinders-->
> HexMeshCylinders generates hexagonal meshes for [OpenFOAM][openfoam-url].  It is restricted to volumes with radial-rotational symmetry, i.e. solids that can be described as a "stack" of cylinders.

[![Build Status][travis-image]][travis-url]

I've created this simple tool after having problems with spurious currents (a.k.a. parasitic currents) in **interFoam**. I was working on microfluidics cases, but the results were not good because spurious currents were deforming the droplets. It is known that regular meshes can attenuate the problems with spurious currents, therefore I wanted to try that. I tried to create these meshes using **blockMesh** and **gmsh**, however, because my volumes were cylindrical (nozzles, reservoirs, etc.), I didn't manage to get what I wanted. So I decided to write this tool.

The problem I was working on was the formation of droplets out of nozzles measuring 50 micrometers in diameter. The regular mesh solved my problems with spurious currents. (I hope to upload a video of it soon).


## Installation

```sh
pip install hexmeshcylinders
```

## Usage example

The following example generates the mesh shown in the image bellow. For more demos, please
 refer to the ``examples`` folder.


```python
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
```

<p align="center">
    <img src="media/basic_1.png" alt="basic_1" width="400"/>
</p>

## Requirements

Requires [numpy][numpy-url]. If you want to run the tests, you will also need to have
 [OpenFOAM][openfoam-git-url] installed.


## Meta

Gui Miotto – [@gmiotto](https://twitter.com/gmiotto)

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/gui-miotto](https://github.com/gui-miotto)

<!-- Markdown link & img dfn's -->
[openfoam-url]: https://www.openfoam.com/
[openfoam-git-url]: https://github.com/OpenFOAM/OpenFOAM-7
[numpy-url]: https://github.com/numpy/numpy
[travis-image]: https://img.shields.io/travis/gui-miotto/HexMeshCylinders/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/github/gui-miotto/HexMeshCylinders
