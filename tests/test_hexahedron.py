import math, os, re, subprocess, unittest
import numpy as np

from HexMeshCylinders import Stack
from HexMeshCylinders.Shapes import Rectangle


class TestHexahedron(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestHexahedron, cls).setUpClass()

        this_dir = os.path.dirname(os.path.abspath( __file__ ))
        case_dir = os.path.join(this_dir, 'dummy_case')
        mesh_dir = os.path.join(case_dir, 'constant', 'polyMesh')

        stack = Stack(cell_edge=.5)

        # Cells of this solid should have a volume of exactly .125
        stack.add_solid(
            shape2d=Rectangle(len_x=5., len_y=10.),
            height=3.,
        )
        # Cells of this solid should have a volume of exactly .625
        stack.add_solid(
            shape2d=Rectangle(len_x=3.),
            height=5.,
            n_layers=2,
        )
        # The total mesh volume should be exactly 195.
        stack.build_mesh()
        stack.export(mesh_dir)

        # Run checkMesh and store its output
        process = subprocess.Popen(
            ['checkMesh', '-case', case_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)
        cls.checkMesh_output, stderr = process.communicate()
        if process.poll() != 0:
            raise RuntimeError(stderr)
        print(cls.checkMesh_output)

    def setUp(self):
        self.checkMesh_output = TestHexahedron.checkMesh_output

    def test_volumes(self):
        checks = [
            'cells:            1272',
            'hexahedra:     1272',
            'Min volume = 0.125. Max volume = 0.625.  Total volume = 195.  Cell volumes OK.',
        ]

        for check in checks:
            self.assertIn(check, self.checkMesh_output,
                          msg=f'couldn\'t find "{check}"')

if __name__ == '__main__':
    unittest.main()
