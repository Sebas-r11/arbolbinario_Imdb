from typing import Optional
from src.models import Pelicula

class NodoPelicula:
    def __init__(self, data: Pelicula):
        self.data: Pelicula = data
        self.right: Optional['NodoPelicula'] = None
        self.left: Optional['NodoPelicula'] = None

    def __repr__(self):
        return f"Node({self.data.id})"
