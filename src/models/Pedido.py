import uuid
from datetime import datetime

from models.Producto import Producto
from models.Usuario import Cliente


class Pedido:
    """Pedido de un cliente con una lista de productos y sus cantidades."""

    def __init__(self, cliente: Cliente, productos: list):
        self.id: str = str(uuid.uuid4())
        self.cliente: Cliente = cliente
        # lista de tuplas (producto, cantidad)
        self.productos: list = productos
        self.fecha: datetime = datetime.now()

    def calcular_total(self) -> float:
        """Calcula el importe total del pedido."""
        total = 0
        for producto, cantidad in self.productos:
            total += producto.precio * cantidad
        return total

    def __str__(self) -> str:
        return f"Pedido de {self.cliente.nombre} ({self.fecha}) - Total: {self.calcular_total()} EUR"
