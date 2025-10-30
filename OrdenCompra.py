from datetime import date
from DetalleOrdenCompra import DetalleOrdenCompra


class OrdenCompra:
    _next_num = 1

    def __init__(self):
        # Fecha del día de hoy
        self.fecha = date.today()
        # Numero autogenerado
        self.numero = OrdenCompra._next_num
        OrdenCompra._next_num += 1
        # Lista de detalles
        self.listaDetalles = []  # list of DetalleOrdenCompra
        self.total = 0.0

    def agregar_detalle(self, detalle: DetalleOrdenCompra):
        self.listaDetalles.append(detalle)
        self._recalcular_total()

    def _recalcular_total(self):
        self.total = sum(getattr(d, 'subtotal', 0.0) for d in self.listaDetalles)

    def __str__(self):
        return f"Orden {self.numero} - Fecha: {self.fecha} - Total: {self.total}"
