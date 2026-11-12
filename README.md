# Tienda online - API REST

**Autora:** María Lombó
**Asignatura:** Arquitectura del Software (UIE)

## Descripción

Aplicación en Python que implementa una tienda online. Permite gestionar usuarios (clientes y administradores), productos (genéricos, electrónicos y de ropa) y pedidos mediante una API REST hecha con FastAPI. Los datos se guardan en memoria mientras el servidor está arrancado.

## Estructura del repositorio

    .
    ├── .gitignore
    ├── requirements.txt
    ├── README.md
    └── src/
        ├── main.py                  # aplicación FastAPI y endpoints
        ├── models/                  # clases del dominio (Producto, Usuario, Pedido)
        ├── Services/                # lógica de la tienda (TiendaService)
        └── schemas/                 # esquemas Pydantic

## Ejecutar

    pip install -r requirements.txt
    cd src
    uvicorn main:app --reload

La API queda en http://localhost:8000 y la documentación en http://localhost:8000/docs

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /usuarios | crea un usuario |
| GET | /usuarios | lista de usuarios |
| GET | /usuarios/{usuario_id} | un usuario |
| POST | /productos | crea un producto (genérico, electrónico o ropa) |
| GET | /productos | lista de productos |
| GET | /productos/{producto_id} | un producto |
| DELETE | /productos/{producto_id} | elimina un producto |
| POST | /pedidos | crea un pedido |
| GET | /usuarios/{cliente_id}/pedidos | pedidos de un cliente |
