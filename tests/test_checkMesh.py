import math, os, re, subprocess, unittest
import numpy as np

from HexMeshCylinders import Stack
from HexMeshCylinders.Shapes import Circle


class TestCheckMesh(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCheckMesh, cls).setUpClass()

        this_dir = os.path.dirname(os.path.abspath( __file__ ))
        case_dir = os.path.join(this_dir, 'dummy_case')
        mesh_dir = os.path.join(case_dir, 'constant', 'polyMesh')

        # Randomly create the specs for some cylinders
        n_cyls = 5
        diams = [6.40638322, 7.66518258, 4.32723791, 6.08662084, 9.14357563]
        heights = [4.68887927, 2.37675593, 2.62172863, 2.15440161, 3.32242953]
        n_layers = [7, 3, 5, 4, 5]

        # Analytically calculate the volume of this stack
        vol = 0.
        for n in range(n_cyls):
            vol += heights[n] * math.pi * (diams[n] / 2.) ** 2.
        cls.analytical_volume = vol

        # Create stack specification
        stack = Stack(cell_edge=.2)
        for n in range(n_cyls):
            stack.add_solid(
                shape2d=Circle(diameter=diams[n]),
                height=heights[n],
                n_layers=n_layers[n],
            )

        # Create mesh and export it
        stack.build_mesh()
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
        self.analytical_volume = TestCheckMesh.analytical_volume
        self.checkMesh_output = TestCheckMesh.checkMesh_output

    def test_total_volume(self):
        # Extract total mesh volume from checkMesh output
        match = re.search(r'Total volume = [0-9]*\.[0-9]*', self.checkMesh_output)
        mesh_vol = float(match.group(0).split(' ')[-1])

        # Difference between analytical and mesh volumes should be small
        rel_error = abs(self.analytical_volume - mesh_vol) / self.analytical_volume
        self.assertLess(rel_error, 0.01)  # 1% tolerance

    def test_oks(self):
        lines = self.checkMesh_output.splitlines()
        checks = [
            'Boundary definition',
            'Point usage',
            'Upper triangular ordering',
            'Face vertices',
            'Topological cell zip-up check',
            'Face-face connectivity',
            'Boundary openness',
            'Max cell openness',
            'Minimum face area = '
            'Min volume = ',
            'Non-orthogonality check',
            'Face pyramids',
            'Max skewness',
            'Coupled point location match',
            'Face tets',
            'Min/max edge length',
            'All angles in faces',
            'All face flatness',
            'Cell determinant check',
            'Concave cell check',
            'Face interpolation weight check',
            'Face volume ratio check',
        ]

        for line in lines:
            for check in checks:
                if line.startswith(check):
                    self.assertTrue(
                        line.endswith(' OK.'),
                        msg=f'Failed at "{check}"')
                    break

    def test_other_one_liners(self):
        checks = [
            'hexahedra:     22212',
            'prisms:        0',
            'wedges:        0',
            'pyramids:      0',
            'tet wedges:    0',
            'tetrahedra:    0',
            'polyhedra:     0',
            'points:           26389',
            'faces:            70664',
            'internal faces:   62608',
            'cells:            22212',
            'faces per cell:   6',
            'boundary patches: 11',
            'Number of regions: 1 (OK).',
            'Mesh OK.'
        ]

        for check in checks:
            self.assertIn(check, self.checkMesh_output,
                          msg=f'couldn\'t find "{check}"')

if __name__ == '__main__':
    unittest.main()
