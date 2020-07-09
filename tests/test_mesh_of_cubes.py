import unittest
import os
import re
import subprocess

from HexMeshCylinders import Stack
from HexMeshCylinders.Shapes import Circle


class TestMeshOfCubes(unittest.TestCase):
    """
    Creates a mesh made just of cubes by using n_layers=None
    """

    @classmethod
    def setUpClass(cls):
        super(TestMeshOfCubes, cls).setUpClass()

        this_dir = os.path.dirname(os.path.abspath(__file__))
        case_dir = os.path.join(this_dir, 'dummy_case')
        mesh_dir = os.path.join(case_dir, 'constant', 'polyMesh')

        # Create stack specification
        diams = [6., 4., 10.]
        heights = [10., 2., 6.]
        stack = Stack(cell_edge=.5)
        for d, h in zip(diams, heights):
            stack.add_solid(
                shape2d=Circle(diameter=d),
                height=h,
            )

        # Create mesh and export it
        stack.build_mesh()
        stack.export(mesh_dir, run_renumberMesh=True)

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
        self.checkMesh_output = TestMeshOfCubes.checkMesh_output

    def test_just_cubes(self):
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

        # All volumes should be the same. i.e. min cell volume = max cell volume
        match = re.search(r'Min volume = [0-9]+\.[0-9]+', self.checkMesh_output)
        min_volume = float(match.group(0).split(' ')[-1])
        match = re.search(r'Max volume = [0-9]+\.[0-9]+', self.checkMesh_output)
        max_volume = float(match.group(0).split(' ')[-1])
        self.assertEqual(min_volume, max_volume)

        # Assert total volume = number of cells * volume of one cell
        match = re.search(r'Total volume = [0-9]+\.[0-9]*', self.checkMesh_output)
        total_volume = float(match.group(0).split(' ')[-1])
        self.assertEqual(hexa_num * min_volume, total_volume)


if __name__ == '__main__':
    unittest.main()
