from typing import Optional

from pydantic import BaseModel


class UsuarioCreate(BaseModel):
    """Datos que envia el cliente para crear un usuario."""
    nombre: str
    email: str
    tipo: str  # "cliente" o "administrador"
    direccion: Optional[str] = None  # solo hace falta para los clientes


class UsuarioRead(BaseModel):
    """Datos que devuelve la API de un usuario."""
    id: str
    nombre: str
    email: str
    es_admin: bool
