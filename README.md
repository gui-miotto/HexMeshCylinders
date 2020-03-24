<p align="center">
  <img src="media/hexmeshcyl.png" alt="hexmeshcyl" width="500"/>
</p>

<!--# HexMeshCylinders-->
> HexMeshCylinders generates hexagonal meshes for [OpenFOAM][openfoam-url].  It is restricted to volumes with radial-rotational symmetry, i.e. solids that can be described as a "stack" of cylinders (see examples bellow).

[![Build Status][travis-image]][travis-url]

One to two paragraph statement about your product and what it does.

## Installation

OS X & Linux:

```sh
npm install my-crazy-module --save
```

Windows:

```sh
edit autoexec.bat
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

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```

## Release History

* 0.2.1
    * CHANGE: Update docs (module code remains unchanged)
* 0.2.0
    * CHANGE: Remove `setDefaultXYZ()`
    * ADD: Add `init()`
* 0.1.1
    * FIX: Crash when calling `baz()` (Thanks @GenerousContributorName!)
* 0.1.0
    * The first proper release
    * CHANGE: Rename `foo()` to `bar()`
* 0.0.1
    * Work in progress

## Meta

Gui Miotto – [@gmiotto](https://twitter.com/gmiotto) – YourEmail@example.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/gui-miotto](https://github.com/gui-miotto)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[openfoam-url]: https://www.openfoam.com/


[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/gui-miotto/HexMeshCylinders/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/github/gui-miotto/HexMeshCylinders
[wiki]: https://github.com/yourname/yourproject/wiki
