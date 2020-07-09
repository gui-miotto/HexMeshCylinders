<p align="center">
  <img src="media/hexmeshcyl.png" alt="hexmeshcyl" width="500"/>
</p>

<!--# HexMeshCylinders-->
> HexMeshCylinders generates hexagonal meshes for [OpenFOAM][openfoam-url]. It is very limited: it can only mesh volumes that can be described as a stack of basic geometric shapes.

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
from HexMeshCylinders import Stack
from HexMeshCylinders.Shapes import Rectangle, Circle

stack = Stack(cell_edge=.015, verbose=True)

stack.add_solid(
    shape2d=Rectangle(len_x=.8, len_y=1.2),
    height=1.,
    n_layers=20,
)
stack.add_solid(
    shape2d=Circle(diameter=.6),
    height=.8,
)

stack.build_mesh()
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
[travis-image]: https://travis-ci.org/gui-miotto/HexMeshCylinders.svg?branch=master
[travis-url]: https://travis-ci.org/gui-miotto/HexMeshCylinders


