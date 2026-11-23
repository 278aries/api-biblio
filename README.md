# API de la Biblioteca

API REST hecha con FastAPI para gestionar los libros de una biblioteca:
crear, listar, buscar, actualizar y borrar.
Los libros se guardan en `datos/libros.json`, así que no se pierden al reiniciar el servidor.

## Estructura

```
api-biblioteca-v1/
├─ main.py           ← la app y las rutas
├─ schemas.py        ← modelos de Pydantic
├─ datos.py          ← leer y guardar datos/libros.json
├─ datos/            ← acá se crea libros.json
├─ requirements.txt
├─ README.md
└─ .gitignore
```

## Instalación

Con Python 3.10 o superior, desde la carpeta del proyecto:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Con el entorno virtual activo:

```bash
fastapi dev main.py
```

O también:

```bash
uvicorn main:app --reload
```

La API queda en http://127.0.0.1:8000 y la documentación en http://127.0.0.1:8000/docs.

## Endpoints

| Método | Ruta | Qué hace |
|--------|------|----------|
| GET | `/` | Mensaje de bienvenida |
| GET | `/libros` | Lista los libros. Filtros `?autor=` y `?disponible=`; paginación `?desde=` y `?limite=` |
| GET | `/libros/buscar?texto=` | Busca el texto en el título o el autor |
| GET | `/libros/estadisticas` | Total de libros, disponibles y prestados |
| POST | `/libros` | Crea un libro (409 si ya existe con el mismo título y autor) |
| GET | `/libros/{id}` | Devuelve un libro |
| PUT | `/libros/{id}` | Reemplaza todos los datos del libro |
| PATCH | `/libros/{id}` | Cambia solo los campos enviados |
| DELETE | `/libros/{id}` | Borra un libro |

## Libro

```json
{
  "id": 1,
  "titulo": "Rayuela",
  "autor": "Julio Cortázar",
  "anio": 1963,
  "disponible": true
}
```

- `id`: lo asigna el servidor, empieza en 1 y no se reutiliza.
- `titulo`: de 3 a 100 caracteres.
- `autor`: de 3 a 60 caracteres.
- `anio`: entre 1000 y 2100.
- `disponible`: `true` si no se envía.
