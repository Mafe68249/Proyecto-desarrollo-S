from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel
from src.database import engine
from fastapi.staticfiles import StaticFiles
from src.models.models import Usuario,Personalidad, KDrama

from src.operations.usuario_operations import (
    create_usuario,
    get_usuarios,
    update_usuario,
    delete_usuario
)

from src.operations.kdrama_operations import (
    create_kdrama,
    get_kdramas,
    update_kdrama,
    delete_kdrama
)

from src.operations.personalidad_operations import (
    create_personalidad,
    get_personalidades,
    update_personalidad,
    delete_personalidad
)

app = FastAPI()
SQLModel.metadata.create_all(engine)
# -----------------------------
# USUARIOS
# -----------------------------

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    return create_usuario(usuario)

@app.get("/usuarios")
def obtener_usuarios():
    return get_usuarios()


@app.get("/usuarios/{id}")
def obtener_usuario(id: int):
    usuarios = get_usuarios()
    for u in usuarios:
        if int(u["id"]) == id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.put("/usuarios/{id}")
def actualizar_usuario(id: int, usuario: Usuario):
    actualizado = update_usuario(id, usuario.model_dump())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return actualizado


@app.delete("/usuarios/{id}")
def eliminar_usuario(id: int):
    eliminado = delete_usuario(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}


@app.get("/usuarios/buscar/{nombre}")
def buscar_usuario(nombre: str):
    usuarios = get_usuarios()
    return [u for u in usuarios if nombre.lower() in u["nombre"].lower()]


# -----------------------------
# KDRAMAS
# -----------------------------

@app.post("/kdramas", response_model=KDrama)
def crear_kdrama(drama: KDrama):
    return create_kdrama(drama.model_dump())


@app.get("/kdramas")
def obtener_kdramas():
    return get_kdramas()


@app.get("/kdramas/{id}")
def obtener_kdrama(id: int):
    dramas = get_kdramas()
    for d in dramas:
        if int(d["id"]) == id:
            return d
    raise HTTPException(status_code=404, detail="K-drama no encontrado")


@app.put("/kdramas/{id}")
def actualizar_kdrama(id: int, drama: KDrama):
    actualizado = update_kdrama(id, drama.model_dump())
    if not actualizado:
        raise HTTPException(status_code=404, detail="K-drama no encontrado")
    return actualizado


@app.delete("/kdramas/{id}")
def eliminar_kdrama(id: int):
    eliminado = delete_kdrama(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="K-drama no encontrado")
    return {"mensaje": "K-drama eliminado"}


@app.get("/kdramas/buscar/{nombre}")
def buscar_kdrama(nombre: str):
    dramas = get_kdramas()
    return [d for d in dramas if nombre.lower() in d["nombre"].lower()]


@app.get("/kdramas/genero/{genero}")
def buscar_genero(genero: str):
    dramas = get_kdramas()
    return [d for d in dramas if genero.lower() in d["genero"].lower()]


# -----------------------------
# PERSONALIDAD
# -----------------------------

@app.post("/personalidad")
def crear_personalidad(p: Personalidad):


    usuarios = get_usuarios()
    existe = any(int(u["id"]) == p.id_usuario for u in usuarios)

    if not existe:
        raise HTTPException(status_code=404, detail="Usuario no existe")

    return create_personalidad(p.model_dump())


@app.get("/personalidad")
def obtener_personalidades():
    return get_personalidades()


@app.get("/personalidad/{id}")
def obtener_personalidad(id: int):
    data = get_personalidades()

    for p in data:
        if int(p["id"]) == id:
            return p

    raise HTTPException(status_code=404, detail="Personalidad no encontrada")


@app.put("/personalidad/{id}")
def actualizar_personalidad(id: int, p: Personalidad):
    actualizado = update_personalidad(id, p.model_dump())

    if not actualizado:
        raise HTTPException(status_code=404, detail="Personalidad no encontrada")

    return actualizado


@app.delete("/personalidad/{id}")
def eliminar_personalidad(id: int):
    eliminado = delete_personalidad(id)

    if not eliminado:
        raise HTTPException(status_code=404, detail="Personalidad no encontrada")

    return {"mensaje": "Personalidad desactivada"}


# -----------------------------
# RECOMENDADOR
# -----------------------------

@app.get("/recomendar/{id_usuario}")
def recomendar(id_usuario: int):

    dramas = get_kdramas()
    personas = get_personalidades()

    personalidad = next(
        (p for p in personas if int(p["id_usuario"]) == id_usuario),
        None
    )

    if not personalidad:
        raise HTTPException(status_code=404, detail="No hay personalidad registrada")

    resultado = []

    for d in dramas:
        genero = d["genero"].lower()


        romantico = str(personalidad["romantico"]) == "True"
        aventurero = str(personalidad["aventurero"]) == "True"
        oscuro = str(personalidad["oscuro"]) == "True"
        intenso = str(personalidad["intenso"]) == "True"

        if romantico and genero == "romance":
            resultado.append(d)

        elif aventurero and genero == "accion":
            resultado.append(d)

        elif oscuro and genero in ["terror", "suspenso"]:
            resultado.append(d)

        elif intenso and int(d["nivel_emocional"]) >= 8:
            resultado.append(d)

    return resultado

