from dataclasses import dataclass


@dataclass
class Producto:
    codigo: int
    denominacion: str
    rubro: str
    marca: str
    precioCompra: float

    def __str__(self):
        return f"{self.codigo} - {self.denominacion} ({self.marca}) {self.rubro} - ${self.precioCompra}"
