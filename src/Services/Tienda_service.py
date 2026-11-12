from models.Producto import Producto
from models.Usuario import Usuario, Cliente, Administrador
from models.Pedido import Pedido


class TiendaService:
    """Gestiona los usuarios, los productos y los pedidos de la tienda."""

    def __init__(self):
        # diccionarios con el id como clave
        self.usuarios: dict = {}
        self.productos: dict = {}
        self.pedidos: list = []

    def registrar_usuario(self, tipo: str, nombre: str, email: str, direccion: str = "") -> Usuario:
        """Registra un usuario de tipo 'cliente' o 'administrador'. Devuelve None si el tipo no es valido."""
        if tipo == "cliente":
            usuario = Cliente(nombre, email, direccion)
        elif tipo == "administrador":
            usuario = Administrador(nombre, email)
        else:
            print("Tipo de usuario no valido")
            return None
        self.usuarios[usuario.id] = usuario
        return usuario

    def obtener_usuario(self, id_usuario: str) -> Usuario:
        """Devuelve el usuario con ese id, o None si no existe."""
        if id_usuario in self.usuarios:
            return self.usuarios[id_usuario]
        return None

    def listar_usuarios(self) -> list:
        """Devuelve una lista con todos los usuarios."""
        lista = []
        for id_usuario in self.usuarios:
            lista.append(self.usuarios[id_usuario])
        return lista

    def obtener_producto(self, id_producto: str) -> Producto:
        """Devuelve el producto con ese id, o None si no existe."""
        if id_producto in self.productos:
            return self.productos[id_producto]
        return None

    def anadir_producto(self, producto: Producto) -> None:
        """Anade un producto al inventario."""
        self.productos[producto.id] = producto

    def eliminar_producto(self, id_producto: str) -> None:
        """Elimina un producto a partir de su id."""
        if id_producto in self.productos:
            self.productos.pop(id_producto)
        else:
            print("El producto no existe")

    def listar_productos(self) -> list:
        """Devuelve una lista con todos los productos."""
        lista = []
        for id_producto in self.productos:
            lista.append(self.productos[id_producto])
        return lista

    def realizar_pedido(self, id_usuario: str, productos: list) -> Pedido:
        """
        Crea un pedido. productos es una lista de tuplas (id_producto, cantidad).
        Devuelve None si el usuario no existe o no hay stock suficiente.
        """
        # comprobamos que el usuario existe
        if id_usuario not in self.usuarios:
            print("El usuario no existe")
            return None
        # el pedido tiene que ser de un cliente
        if not isinstance(self.usuarios[id_usuario], Cliente):
            print("Solo los clientes pueden hacer pedidos")
            return None

        # comprobamos que hay stock de todos los productos
        lineas = []
        for id_producto, cantidad in productos:
            if id_producto not in self.productos:
                print("El producto no existe")
                return None
            producto = self.productos[id_producto]
            if not producto.hay_stock(cantidad):
                print(f"No hay stock suficiente de {producto.nombre}")
                return None
            lineas.append((producto, cantidad))

        # descontamos el stock y creamos el pedido
        for producto, cantidad in lineas:
            producto.actualizar_stock(-cantidad)
        pedido = Pedido(self.usuarios[id_usuario], lineas)
        self.pedidos.append(pedido)
        return pedido

    def listar_pedidos_usuario(self, id_usuario: str) -> list:
        """Devuelve los pedidos de un usuario por orden de fecha."""
        # los pedidos se guardan en el orden en que se crean, asi que ya estan ordenados por fecha
        lista = []
        for pedido in self.pedidos:
            if pedido.cliente.id == id_usuario:
                lista.append(pedido)
        return lista
