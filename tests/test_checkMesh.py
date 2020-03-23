import math, os, re, subprocess, unittest
import numpy as np

from HexMeshCylinders import Cylinder, Stack


class TestCheckMesh(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCheckMesh, cls).setUpClass()

        this_dir = os.path.dirname(os.path.abspath( __file__ ))
        case_dir = os.path.join(this_dir, 'dummy_case')
        mesh_dir = os.path.join(case_dir, 'constant', 'polyMesh')

        # Randomly create the specs for some cylinders
        n_cyls = 5
        rand = np.random.RandomState(0)
        diams = rand.uniform(low=2., high=10., size=n_cyls)
        heights = rand.uniform(low=2., high=10., size=n_cyls)

        # Analytically calculate the volume of this stack
        vol = 0.
        for n in range(n_cyls):
            vol += heights[n] * math.pi * (diams[n] / 2.) ** 2.
        cls.analytical_volume = vol

        # Creat stack specification
        Cylinder.cell_edge = .5
        n_layers = rand.randint(low=1, high=4, size=n_cyls)

        cylinders = list()
        for n in range(n_cyls):
            d = Cylinder.conv_diam(diams[n])
            h = heights[n]
            l = n_layers[n]
            cylinders.append(Cylinder(diameter=d, height=h, n_layers=l))

        # Create mesh and export it
        stack = Stack(cylinders, verbose=False)
        stack.export(mesh_dir)

        # Run checkMesh and store its output
        checkmesh_path = os.path.join(this_dir, 'checkMeshBinary')

        process = subprocess.Popen(
            [checkmesh_path, '-allGeometry', '-allTopology', '-case', case_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)
        cls.checkMesh_output, stderr = process.communicate()
        if process.poll() != 0:
            raise RuntimeError(stderr)
        print(cls.checkMesh_output)

        #stream = os.popen(f'{checkmesh_path} -allGeometry -allTopology -case {case_dir}')
        #cls.checkMesh_output = stream.read()
        #print(cls.checkMesh_output)

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

    def test_only_hexahedra(self):
        match = re.search(r'hexahedra:[ ]*[0-9]*', self.checkMesh_output)
        hexa_num = int(match.group(0).split(' ')[-1])

        # Number of hexahedrals should be greater than zero
        self.assertGreater(hexa_num, 0)

        # Number of any other shape should be zero
        other_shapes = ['prisms', 'wedges', 'pyramids', 'tet wedges',
                        'tetrahedra', 'polyhedra']
        for shape in other_shapes:
            match = re.search(shape + ':[ ]*[0-9]*', self.checkMesh_output)
            shape_num = int(match.group(0).split(' ')[-1])
            self.assertEqual(shape_num, 0, msg=shape)

    def test_one_line_checks(self):
        checks = [
            'faces per cell:   6',
            'boundary patches: 11',
            'Boundary definition OK.',
            'Point usage OK.',
            'Upper triangular ordering OK.',
            'Face vertices OK.',
            'Topological cell zip-up check OK.',
            'Face-face connectivity OK.',
            'Number of regions: 1 (OK).',
            'Max cell openness = 0 OK.',
            'Face area magnitudes OK.',
            'Cell volumes OK.',
            'Non-orthogonality check OK.',
            'Face pyramids OK.',
            'Coupled point location match (average 0) OK.',
            'Face tets OK.',
            'All angles in faces OK.',
            'All face flatness OK.',
            'Cell determinant check OK.',
            'Concave cell check OK.',
            'Face interpolation weight check OK.',
            'Face volume ratio check OK.',
            'Mesh OK.',
        ]

        for check in checks:
            self.assertIn(check, self.checkMesh_output,
                          msg=f'couldn\'t find "{check}"')

if __name__ == '__main__':
    unittest.main()
