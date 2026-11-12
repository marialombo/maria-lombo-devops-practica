# Tienda online - API REST con Docker

**Autora:** María Lombó
**Asignatura:** Arquitectura del Software (UIE)

## Descripción

Aplicación en Python que implementa una tienda online. Permite gestionar usuarios (clientes y administradores), productos (genéricos, electrónicos y de ropa) y pedidos mediante una API REST hecha con FastAPI. Los datos se guardan en memoria mientras el servidor está arrancado.

La aplicación se puede ejecutar directamente con Python o dentro de un contenedor Docker.

## Estructura del repositorio

    .
    ├── Dockerfile
    ├── .dockerignore
    ├── .gitignore
    ├── requirements.txt
    ├── README.md
    └── src/
        ├── main.py                  # aplicación FastAPI y endpoints
        ├── models/                  # clases del dominio (Producto, Usuario, Pedido)
        ├── Services/                # lógica de la tienda (TiendaService)
        └── schemas/                 # esquemas Pydantic

## Ejecutar sin Docker

    pip install -r requirements.txt
    cd src
    uvicorn main:app --reload

La API queda en http://localhost:8000 y la documentación en http://localhost:8000/docs

## Docker

### Construir la imagen

Desde la raíz del repositorio:

    docker build -t tienda-online:1.0 .

### Ejecutar el contenedor

    docker run --name tienda -p 8000:8000 tienda-online:1.0

`-p 8000:8000` publica el puerto 8000 del contenedor en el 8000 de tu ordenador. Dentro del contenedor la API escucha en `0.0.0.0:8000`.

Con otro puerto en tu ordenador (por ejemplo el 9000):

    docker run --name tienda -p 9000:8000 tienda-online:1.0

Gestionar el contenedor:

    docker ps
    docker logs tienda
    docker stop tienda
    docker start tienda
    docker rm tienda

### Variables de entorno

La aplicación no usa variables de entorno, por lo que no hay que configurar nada al ejecutarla.

### Probar que funciona

Al arrancar, en la terminal debe aparecer algo como:

    INFO:     Uvicorn running on http://0.0.0.0:8000

Después se puede probar:

1. Abrir http://localhost:8000/docs (documentación interactiva de la API).
2. Crear un producto:

        curl -X POST http://localhost:8000/productos \
          -H "Content-Type: application/json" \
          -d '{"tipo": "generico", "nombre": "Taza", "precio": 5, "stock": 30}'

   Debe responder con código 201 y los datos del producto con su `id`.
3. Listar los productos: `curl http://localhost:8000/productos` (código 200).
4. Consultar un producto que no existe: `curl http://localhost:8000/productos/xxx` (código 404).

### Endpoints

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

### Descargar la imagen publicada (pull)

La imagen está publicada en Docker Hub:

    docker pull TU_USUARIO_DOCKERHUB/tienda-online:1.0
    docker run --name tienda -p 8000:8000 TU_USUARIO_DOCKERHUB/tienda-online:1.0

### Publicar la imagen (push)

    docker login
    docker tag tienda-online:1.0 TU_USUARIO_DOCKERHUB/tienda-online:1.0
    docker push TU_USUARIO_DOCKERHUB/tienda-online:1.0

## Flujo de trabajo con Git

- `main`: rama principal, siempre con código funcional.
- `feature/docker`: rama donde se añadió la contenedorización. Se integró en `main` mediante Pull Request.
