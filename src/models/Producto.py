import uuid


class Producto:
    """Clase padre para todos los productos de la tienda."""

    def __init__(self, nombre: str, precio: float, stock: int):
        # el id se genera automaticamente al crear el producto
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock

    def hay_stock(self, cantidad: int) -> bool:
        """Devuelve True si hay stock suficiente para la cantidad pedida."""
        return self.stock >= cantidad

    def actualizar_stock(self, cantidad: int) -> None:
        """Suma la cantidad al stock (positiva para reponer, negativa para compras)."""
        self.stock += cantidad

    def __str__(self) -> str:
        return f"{self.nombre} - {self.precio} EUR - stock: {self.stock}"


class ProductoElectronico(Producto):
    """Producto electronico con meses de garantia."""

    def __init__(self, nombre: str, precio: float, stock: int, garantia: int):
        super().__init__(nombre, precio, stock)
        self.garantia: int = garantia

    def __str__(self) -> str:
        return f"{self.nombre} - {self.precio} EUR - stock: {self.stock} - garantia: {self.garantia} meses"


class ProductoRopa(Producto):
    """Producto de ropa con talla y color."""

    def __init__(self, nombre: str, precio: float, stock: int, talla: str, color: str):
        super().__init__(nombre, precio, stock)
        self.talla: str = talla
        self.color: str = color

    def __str__(self) -> str:
        return f"{self.nombre} - {self.precio} EUR - stock: {self.stock} - talla: {self.talla} - color: {self.color}"
