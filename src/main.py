from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from Services.Tienda_service import TiendaService
from models.Producto import Producto, ProductoElectronico, ProductoRopa
from models.Usuario import Cliente
from schemas.Usuario import UsuarioCreate, UsuarioRead
from schemas.Producto import ProductoCreate, ProductoRead
from schemas.Pedido import PedidoCreate, PedidoRead, PedidoItemRead

app = FastAPI(title="Tienda online", description="API REST de la tienda online (Practica 2)")

# permite que el frontend (otra pagina en el navegador) pueda llamar a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# una unica tienda, los datos se guardan en memoria mientras el servidor esta arrancado
tienda = TiendaService()


# ---------------------------------------------------------------
# funciones auxiliares: pasan de objetos del dominio a esquemas
# ---------------------------------------------------------------

def usuario_a_read(usuario) -> UsuarioRead:
    return UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        es_admin=usuario.is_admin(),
    )


def producto_a_read(producto) -> ProductoRead:
    tipo = "generico"
    meses_garantia = None
    talla = None
    color = None
    if isinstance(producto, ProductoElectronico):
        tipo = "electronico"
        meses_garantia = producto.garantia
    elif isinstance(producto, ProductoRopa):
        tipo = "ropa"
        talla = producto.talla
        color = producto.color
    return ProductoRead(
        id=producto.id,
        tipo=tipo,
        nombre=producto.nombre,
        precio=producto.precio,
        stock=producto.stock,
        meses_garantia=meses_garantia,
        talla=talla,
        color=color,
    )


def pedido_a_read(pedido) -> PedidoRead:
    items = []
    for producto, cantidad in pedido.productos:
        items.append(PedidoItemRead(
            producto_id=producto.id,
            nombre=producto.nombre,
            precio=producto.precio,
            cantidad=cantidad,
            subtotal=producto.precio * cantidad,
        ))
    return PedidoRead(
        id=pedido.id,
        fecha=pedido.fecha,
        cliente=usuario_a_read(pedido.cliente),
        total=pedido.calcular_total(),
        items=items,
    )


# ---------------------------------------------------------------
# Usuarios
# ---------------------------------------------------------------

@app.post("/usuarios", response_model=UsuarioRead, status_code=201)
def crear_usuario(datos: UsuarioCreate):
    if datos.tipo not in ("cliente", "administrador"):
        raise HTTPException(status_code=400, detail="El tipo debe ser 'cliente' o 'administrador'")
    if datos.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacio")
    if "@" not in datos.email:
        raise HTTPException(status_code=400, detail="El email no es valido")
    if datos.tipo == "cliente" and not datos.direccion:
        raise HTTPException(status_code=400, detail="Un cliente necesita direccion")

    direccion = datos.direccion
    if direccion is None:
        direccion = ""
    usuario = tienda.registrar_usuario(datos.tipo, datos.nombre, datos.email, direccion)
    return usuario_a_read(usuario)


@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios():
    lista = []
    for usuario in tienda.listar_usuarios():
        lista.append(usuario_a_read(usuario))
    return lista


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: str):
    usuario = tienda.obtener_usuario(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    return usuario_a_read(usuario)


# ---------------------------------------------------------------
# Productos
# ---------------------------------------------------------------

@app.post("/productos", response_model=ProductoRead, status_code=201)
def crear_producto(datos: ProductoCreate):
    if datos.tipo not in ("generico", "electronico", "ropa"):
        raise HTTPException(status_code=400, detail="El tipo debe ser 'generico', 'electronico' o 'ropa'")
    if datos.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacio")
    if datos.precio <= 0:
        raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0")
    if datos.stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo")

    # cada tipo necesita sus propios atributos
    if datos.tipo == "electronico":
        if datos.meses_garantia is None or datos.meses_garantia < 0:
            raise HTTPException(status_code=400, detail="Un producto electronico necesita meses_garantia (0 o mas)")
        producto = ProductoElectronico(datos.nombre, datos.precio, datos.stock, datos.meses_garantia)
    elif datos.tipo == "ropa":
        if not datos.talla or not datos.color:
            raise HTTPException(status_code=400, detail="Un producto de ropa necesita talla y color")
        producto = ProductoRopa(datos.nombre, datos.precio, datos.stock, datos.talla, datos.color)
    else:
        producto = Producto(datos.nombre, datos.precio, datos.stock)

    tienda.anadir_producto(producto)
    return producto_a_read(producto)


@app.get("/productos", response_model=List[ProductoRead])
def listar_productos():
    lista = []
    for producto in tienda.listar_productos():
        lista.append(producto_a_read(producto))
    return lista


@app.get("/productos/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: str):
    producto = tienda.obtener_producto(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="El producto no existe")
    return producto_a_read(producto)


@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: str):
    if tienda.obtener_producto(producto_id) is None:
        raise HTTPException(status_code=404, detail="El producto no existe")
    tienda.eliminar_producto(producto_id)
    return {"mensaje": "Producto eliminado"}


# ---------------------------------------------------------------
# Pedidos
# ---------------------------------------------------------------

@app.post("/pedidos", response_model=PedidoRead, status_code=201)
def crear_pedido(datos: PedidoCreate):
    # el cliente tiene que existir y ser un cliente (no un administrador)
    usuario = tienda.obtener_usuario(datos.cliente_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    if not isinstance(usuario, Cliente):
        raise HTTPException(status_code=400, detail="Solo los clientes pueden hacer pedidos")
    if len(datos.items) == 0:
        raise HTTPException(status_code=400, detail="El pedido no tiene productos")

    # sumamos las cantidades por si un mismo producto aparece en varias lineas
    cantidades = {}
    for item in datos.items:
        if item.cantidad <= 0:
            raise HTTPException(status_code=400, detail="La cantidad debe ser mayor que 0")
        if tienda.obtener_producto(item.producto_id) is None:
            raise HTTPException(status_code=404, detail=f"El producto {item.producto_id} no existe")
        if item.producto_id in cantidades:
            cantidades[item.producto_id] += item.cantidad
        else:
            cantidades[item.producto_id] = item.cantidad

    # comprobamos que hay stock de cada producto
    lineas = []
    for id_producto in cantidades:
        producto = tienda.obtener_producto(id_producto)
        if not producto.hay_stock(cantidades[id_producto]):
            raise HTTPException(status_code=400, detail=f"No hay stock suficiente de {producto.nombre}")
        lineas.append((id_producto, cantidades[id_producto]))

    pedido = tienda.realizar_pedido(datos.cliente_id, lineas)
    if pedido is None:
        raise HTTPException(status_code=400, detail="No se ha podido crear el pedido")
    return pedido_a_read(pedido)


@app.get("/usuarios/{cliente_id}/pedidos", response_model=List[PedidoRead])
def listar_pedidos_cliente(cliente_id: str):
    if tienda.obtener_usuario(cliente_id) is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    lista = []
    for pedido in tienda.listar_pedidos_usuario(cliente_id):
        lista.append(pedido_a_read(pedido))
    return lista
