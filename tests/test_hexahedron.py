import unittest
import os
import subprocess

from HexMeshCylinders import Stack
from HexMeshCylinders.Shapes import Rectangle


class TestHexahedron(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestHexahedron, cls).setUpClass()

        this_dir = os.path.dirname(os.path.abspath(__file__))
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

        # Edit boundaries. At the end, there should be 8 patches
        be = stack.get_boundary_editor()
        be.split_boundaries_coord(index=0, coord_name='y', coord_value=0.)
        be.split_boundaries_coord(index=0, coord_name='z', coord_value=2., new_names=('h1', 'h2'))
        be.split_boundaries_coord(index=0, coord_name='x', coord_value=1., new_types=('wall', 'patch'))

        # Export mesh
        stack.export(mesh_dir)

        # Run checkMesh and store its output
        process = subprocess.Popen(
            ['checkMesh', '-allGeometry', '-allTopology', '-case', case_dir],
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

    def test_boundary_editor(self):
        checks = [
            'boundary patches: 8',
            'boundary_3          48       72       ok (non-closed singly connected)   '
            '(-1.5 -1.5 3) (1.5 1.5 8)',
            'boundary_4          36       49       ok (non-closed singly connected)   '
            '(-1.5 -1.5 8) (1.5 1.5 8)',
            'boundary_0_a        100      121      ok (non-closed singly connected)   '
            '(-2.5 0 0) (2.5 5 0)',
            'boundary_0_b        100      121      ok (non-closed singly connected)   '
            '(-2.5 -5 0) (2.5 0 0)',
            'h1                  120      180      ok (non-closed singly connected)   '
            '(-2.5 -5 2) (2.5 5 3)',
            'h2                  240      300      ok (non-closed singly connected)   '
            '(-2.5 -5 0) (2.5 5 2)',
            'boundary_2_a        54       79       ok (non-closed singly connected)   '
            '(1 -5 3) (2.5 5 3)',
            'boundary_2_b        110      143      ok (non-closed singly connected)   '
            '(-2.5 -5 3) (1 5 3)',
            ]

        for check in checks:
            self.assertIn(check, self.checkMesh_output,
                          msg=f'couldn\'t find "{check}"')


if __name__ == '__main__':
    unittest.main()
