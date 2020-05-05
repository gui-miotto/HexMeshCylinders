from typing import Tuple


class Face():
    def __init__(self,
                 vertex: Tuple[int, int, int, int],
                 owner: int,
                 orientation: str,
                 neighbour: int = None,
                 ):
        self.vertex = vertex
        self.owner = owner
        self.neighbour = neighbour
        self.orientation = orientation
