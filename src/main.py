from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import SQLModel
from src.database import engine, create_tables
from src.models.models import Usuario, Personalidad, KDrama
import os


from src.operations.usuario_operations import (
    create_usuario,
    get_usuarios,
    update_usuario,
    delete_usuario,
    get_usuario_by_email
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

# ========== AUTENTICACIÓN ==========
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

# ========== CREAR TABLAS ==========
create_tables()  # ✅ CORREGIDO: ahora usa la función

# ========== SERVIR ARCHIVOS ESTÁTICOS ==========
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")


# ========== CONFIGURACIÓN JWT ==========
SECRET_KEY = "tu-clave-secreta-cambiala-en-produccion-123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    from src.operations.usuario_operations import get_usuarios
    usuarios = get_usuarios()
    user = next((u for u in usuarios if int(u["id"]) == int(user_id)), None)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


def get_current_admin(current_user=Depends(get_current_user)):
    if current_user.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    return current_user


# ========== RUTAS DEL FRONTEND ==========
@app.get("/")
async def index():
    return FileResponse("frontend/index.html")


@app.get("/{html_file}")
async def serve_html(html_file: str):
    if html_file.endswith('.html'):
        file_path = f"frontend/{html_file}"
        if os.path.exists(file_path):
            return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Página no encontrada")


# ========== AUTENTICACIÓN ==========

@app.post("/login")
def login(email: str, password: str):
    from src.operations.usuario_operations import get_usuario_by_email

    print(f"Intentando login con email: {email}")

    usuario = get_usuario_by_email(email)
    if not usuario:
        print("Usuario no encontrado")
        raise HTTPException(status_code=401, detail="Email incorrecto")

    print(f"Usuario encontrado: {usuario.nombre}")

    if not verify_password(password, usuario.password):
        print("Contraseña incorrecta")
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = create_access_token({"sub": str(usuario.id), "rol": usuario.rol})

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario_id": usuario.id,
        "nombre": usuario.nombre,
        "rol": usuario.rol
    }

@app.get("/usuarios/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user


# ========== REGISTRO DE USUARIOS ==========
@app.post("/registro")
def registro(nombre: str, edad: int, email: str, password: str):
    from src.operations.usuario_operations import get_usuario_by_email, create_usuario
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Verificar si ya existe
    existe = get_usuario_by_email(email)
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Encriptar contraseña
    hashed_password = pwd_context.hash(password)

    # Crear usuario (rol por defecto "usuario")
    nuevo_usuario = create_usuario({
        "nombre": nombre,
        "edad": edad,
        "email": email,
        "password": hashed_password,
        "rol": "usuario"
    })

    return {"mensaje": "Usuario creado exitosamente", "usuario": nuevo_usuario}

# ========== USUARIOS (PÚBLICOS) ==========
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


@app.get("/usuarios/buscar/{nombre}")
def buscar_usuario(nombre: str):
    usuarios = get_usuarios()
    return [u for u in usuarios if nombre.lower() in u["nombre"].lower()]


# ========== USUARIOS (SOLO ADMIN) ==========
@app.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario, admin=Depends(get_current_admin)):
    return create_usuario(usuario)


@app.put("/usuarios/{id}")
def actualizar_usuario(id: int, usuario: Usuario, admin=Depends(get_current_admin)):
    actualizado = update_usuario(id, usuario.model_dump())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return actualizado


@app.delete("/usuarios/{id}")
def eliminar_usuario(id: int, admin=Depends(get_current_admin)):
    eliminado = delete_usuario(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}


# ========== KDRAMAS (PÚBLICOS) ==========
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


@app.get("/kdramas/buscar/{nombre}")
def buscar_kdrama(nombre: str):
    dramas = get_kdramas()
    return [d for d in dramas if nombre.lower() in d["nombre"].lower()]


@app.get("/kdramas/genero/{genero}")
def buscar_genero(genero: str):
    dramas = get_kdramas()
    return [d for d in dramas if genero.lower() in d["genero"].lower()]


# ========== KDRAMAS (SOLO ADMIN) ==========
@app.post("/kdramas", response_model=KDrama)
def crear_kdrama(drama: KDrama, admin=Depends(get_current_admin)):
    return create_kdrama(drama.model_dump())


@app.put("/kdramas/{id}")
def actualizar_kdrama(id: int, drama: KDrama, admin=Depends(get_current_admin)):
    actualizado = update_kdrama(id, drama.model_dump())
    if not actualizado:
        raise HTTPException(status_code=404, detail="K-drama no encontrado")
    return actualizado


@app.delete("/kdramas/{id}")
def eliminar_kdrama(id: int, admin=Depends(get_current_admin)):
    eliminado = delete_kdrama(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="K-drama no encontrado")
    return {"mensaje": "K-drama eliminado"}


# ========== PERSONALIDAD (PÚBLICOS) ==========
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


# ========== PERSONALIDAD (SOLO ADMIN) ==========
@app.post("/personalidad")
def crear_personalidad(p: Personalidad, admin=Depends(get_current_admin)):
    usuarios = get_usuarios()
    existe = any(int(u["id"]) == p.id_usuario for u in usuarios)
    if not existe:
        raise HTTPException(status_code=404, detail="Usuario no existe")
    return create_personalidad(p.model_dump())


@app.put("/personalidad/{id}")
def actualizar_personalidad(id: int, p: Personalidad, admin=Depends(get_current_admin)):
    actualizado = update_personalidad(id, p.model_dump())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Personalidad no encontrada")
    return actualizado


@app.delete("/personalidad/{id}")
def eliminar_personalidad(id: int, admin=Depends(get_current_admin)):
    eliminado = delete_personalidad(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Personalidad no encontrada")
    return {"mensaje": "Personalidad desactivada"}


# ========== PERSONALIDAD PARA USUARIO LOGUEADO ==========
@app.get("/personalidad/mi-personalidad")
def mi_personalidad(current_user=Depends(get_current_user)):
    personalidades = get_personalidades()
    mi_personalidad = next(
        (p for p in personalidades if int(p["id_usuario"]) == current_user["id"]),
        None
    )
    if not mi_personalidad:
        return {"mensaje": "No tienes personalidad registrada", "tiene": False}
    return {"tiene": True, "personalidad": mi_personalidad}


@app.post("/personalidad/mi-personalidad")
def crear_mi_personalidad(personalidad_data: dict, current_user=Depends(get_current_user)):
    personalidades = get_personalidades()
    existe = next(
        (p for p in personalidades if int(p["id_usuario"]) == current_user["id"]),
        None
    )

    personalidad_data["id_usuario"] = current_user["id"]

    if existe:
        actualizado = update_personalidad(existe["id"], personalidad_data)
        return {"mensaje": "Personalidad actualizada", "personalidad": actualizado}
    else:
        nueva = create_personalidad(personalidad_data)
        return {"mensaje": "Personalidad creada", "personalidad": nueva}


# ========== RECOMENDADOR (PÚBLICO PARA ADMIN) ==========
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


# ========== RECOMENDACIONES PARA USUARIO LOGUEADO ==========
@app.get("/recomendar/mis-recomendaciones")
def mis_recomendaciones(current_user=Depends(get_current_user)):
    dramas = get_kdramas()
    personalidades = get_personalidades()

    mi_personalidad = next(
        (p for p in personalidades if int(p["id_usuario"]) == current_user["id"]),
        None
    )

    if not mi_personalidad:
        raise HTTPException(status_code=404, detail="No tienes personalidad registrada")

    resultado = []
    for d in dramas:
        genero = d["genero"].lower()
        romantico = mi_personalidad.get("romantico", False)
        aventurero = mi_personalidad.get("aventurero", False)
        oscuro = mi_personalidad.get("oscuro", False)
        intenso = mi_personalidad.get("intenso", False)

        if romantico and genero == "romance":
            resultado.append(d)
        elif aventurero and genero == "accion":
            resultado.append(d)
        elif oscuro and genero in ["terror", "suspenso"]:
            resultado.append(d)
        elif intenso and int(d["nivel_emocional"]) >= 8:
            resultado.append(d)

    return {"recomendaciones": resultado, "total": len(resultado)}