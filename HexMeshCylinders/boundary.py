class Boundary():
    def __init__(self, name, faces, b_type='patch'):
        self.name = name
        self.faces = faces
        self.b_type = b_type

    def __iter__(self):
        return self.faces.__iter__()

    def __getitem__(self, key):
        return self.faces[key]

    def __len__(self):
        return len(self.faces)
