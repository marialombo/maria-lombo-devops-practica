# Tienda online - API REST con Docker

**Autora:** María Lombó

API REST en Python (FastAPI) de una tienda online que gestiona usuarios, productos y pedidos. Los datos se guardan en memoria.

## Construir la imagen

    docker build -t tienda-online:1.0 .

## Ejecutar

    docker run --name tienda -p 8000:8000 tienda-online:1.0

Para usar otro puerto en el ordenador: `docker run --name tienda -p 9000:8000 tienda-online:1.0`

## Variables de entorno

La aplicación no usa variables de entorno.

## Prueba

Al arrancar debe aparecer:

    INFO:     Uvicorn running on http://0.0.0.0:8000

Después se abre http://localhost:8000/docs y se prueban los endpoints, por ejemplo `GET /productos`.

## Descargar la imagen (pull)

    docker pull marialombo/tienda-online:1.0
    docker run --name tienda -p 8000:8000 marialombo/tienda-online:1.0
