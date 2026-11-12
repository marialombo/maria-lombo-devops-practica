from typing import Optional

from pydantic import BaseModel


class ProductoCreate(BaseModel):
    """Datos que envia el cliente para crear un producto."""
    tipo: str  # "generico", "electronico" o "ropa"
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None  # solo para electronico
    talla: Optional[str] = None  # solo para ropa
    color: Optional[str] = None  # solo para ropa


class ProductoRead(BaseModel):
    """Datos que devuelve la API de un producto."""
    id: str
    tipo: str
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None
