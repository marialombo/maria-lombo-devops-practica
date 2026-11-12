from datetime import datetime
from typing import List

from pydantic import BaseModel

from schemas.Usuario import UsuarioRead


class PedidoItemCreate(BaseModel):
    """Una linea del pedido al crearlo: producto y cantidad."""
    producto_id: str
    cantidad: int


class PedidoCreate(BaseModel):
    """Datos que envia el cliente para crear un pedido."""
    cliente_id: str
    items: List[PedidoItemCreate]


class PedidoItemRead(BaseModel):
    """Una linea del pedido en la respuesta."""
    producto_id: str
    nombre: str
    precio: float
    cantidad: int
    subtotal: float


class PedidoRead(BaseModel):
    """Datos que devuelve la API de un pedido."""
    id: str
    fecha: datetime
    cliente: UsuarioRead
    total: float
    items: List[PedidoItemRead]
