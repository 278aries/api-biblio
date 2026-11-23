import json
from pathlib import Path

from schemas import LibroConId

# El archivo queda junto a main.py, sin importar desde dónde se ejecute.
RUTA = Path(__file__).parent / "datos" / "libros.json"


def cargar():
    # Si el archivo no existe, está vacío o dañado, se arranca con la lista vacía.
    try:
        datos = json.loads(RUTA.read_text(encoding="utf-8"))
        libros = [LibroConId(**d).model_dump() for d in datos]
    except (OSError, ValueError, TypeError):
        return []
    return sorted(libros, key=lambda l: l["id"])


def guardar(libros):
    RUTA.parent.mkdir(exist_ok=True)
    RUTA.write_text(json.dumps(libros, indent=2, ensure_ascii=False), encoding="utf-8")
