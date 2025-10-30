from dataclasses import dataclass
from Producto import Producto 


@dataclass
class DetalleOrdenCompra:
    cantidad: int
    producto: Producto

    def __post_init__(self):
        if self.cantidad < 1:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        self.subtotal = self.cantidad * float(self.producto.precioCompra)

    def __str__(self):
        p = self.producto
        return f"{p.codigo} {p.denominacion} {p.rubro} {p.marca} {self.cantidad} {self.subtotal}"
