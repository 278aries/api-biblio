from fastapi import FastAPI, HTTPException

from datos import cargar, guardar
from schemas import Libro, LibroConId, LibroParcial

app = FastAPI()

libros = cargar()
proximo_id = max([l["id"] for l in libros], default=0) + 1


def buscar_libro(id: int):
    for libro in libros:
        if libro["id"] == id:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.get("/")
def inicio():
    return {"mensaje": "API de la biblioteca"}


@app.get("/libros", response_model=list[LibroConId])
def listar_libros(
    autor: str | None = None,
    disponible: bool | None = None,
    desde: int = 0,
    limite: int = 100,
):
    resultado = libros
    if autor is not None:
        resultado = [l for l in resultado if l["autor"].lower() == autor.lower()]
    if disponible is not None:
        resultado = [l for l in resultado if l["disponible"] == disponible]
    return resultado[desde : desde + limite]


@app.get("/libros/buscar", response_model=list[LibroConId])
def buscar_libros(texto: str):
    texto = texto.lower()
    return [
        l for l in libros if texto in l["titulo"].lower() or texto in l["autor"].lower()
    ]


@app.post("/libros", status_code=201, response_model=LibroConId)
def crear_libro(libro: Libro):
    global proximo_id
    for l in libros:
        if (
            l["titulo"].lower() == libro.titulo.lower()
            and l["autor"].lower() == libro.autor.lower()
        ):
            raise HTTPException(status_code=409, detail="El libro ya existe")
    nuevo = {"id": proximo_id, **libro.model_dump()}
    proximo_id += 1
    libros.append(nuevo)
    guardar(libros)
    return nuevo


@app.get("/libros/{id}", response_model=LibroConId)
def obtener_libro(id: int):
    return buscar_libro(id)


@app.put("/libros/{id}", response_model=LibroConId)
def reemplazar_libro(id: int, datos: Libro):
    libro = buscar_libro(id)
    libro.update(datos.model_dump())
    guardar(libros)
    return libro


@app.patch("/libros/{id}", response_model=LibroConId)
def actualizar_libro(id: int, datos: LibroParcial):
    libro = buscar_libro(id)
    cambios = datos.model_dump(exclude_unset=True)
    if None in cambios.values():
        raise HTTPException(status_code=422, detail="Los campos no pueden ser null")
    libro.update(cambios)
    guardar(libros)
    return libro


@app.delete("/libros/{id}", status_code=204)
def borrar_libro(id: int):
    libros.remove(buscar_libro(id))
    guardar(libros)
