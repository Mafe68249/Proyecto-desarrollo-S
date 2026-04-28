import csv
import os

# -----------------------------
# RUTAS
# -----------------------------
BASE_PATH = "data"

USUARIOS_FILE = os.path.join(BASE_PATH, "usuarios.csv")
KDRAMAS_FILE = os.path.join(BASE_PATH, "kdramas.csv")
PERSONALIDAD_FILE = os.path.join(BASE_PATH, "personalidad.csv")


# -----------------------------
# GENERADOR DE ID
# -----------------------------
def generar_id(file_path):
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = list(csv.DictReader(file))
            if not reader:
                return 1
            return int(reader[-1]["id"]) + 1
    except FileNotFoundError:
        return 1


# =============================
# USUARIOS
# =============================

def read_usuarios():
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def save_usuarios(data):
    with open(USUARIOS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "nombre", "edad", "estado"])
        writer.writeheader()
        writer.writerows(data)


def create_usuario(usuario):
    usuario["id"] = generar_id(USUARIOS_FILE)
    usuario["estado"] = "activo"

    data = read_usuarios()
    data.append(usuario)
    save_usuarios(data)

    return usuario


def get_usuarios():
    data = read_usuarios()
    return [u for u in data if u.get("estado") == "activo"]


def update_usuario(id, nuevo):
    data = read_usuarios()
    encontrado = False

    for u in data:
        if int(u["id"]) == id and u["estado"] == "activo":
            u["nombre"] = nuevo["nombre"]
            u["edad"] = nuevo["edad"]
            encontrado = True
            break

    if not encontrado:
        return None

    save_usuarios(data)
    return nuevo


def delete_usuario(id):
    data = read_usuarios()
    encontrado = False

    for u in data:
        if int(u["id"]) == id:
            u["estado"] = "inactivo"
            encontrado = True
            break

    if not encontrado:
        return False

    save_usuarios(data)
    return True


# =============================
# KDRAMAS
# =============================

def read_kdramas():
    try:
        with open(KDRAMAS_FILE, "r", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def save_kdramas(data):
    with open(KDRAMAS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "nombre", "genero", "nivel_emocional", "estado"])
        writer.writeheader()
        writer.writerows(data)


def create_kdrama(drama):
    drama["id"] = generar_id(KDRAMAS_FILE)
    drama["estado"] = "activo"

    data = read_kdramas()
    data.append(drama)
    save_kdramas(data)

    return drama


def get_kdramas():
    data = read_kdramas()
    return [d for d in data if d.get("estado") == "activo"]


def update_kdrama(id, nuevo):
    data = read_kdramas()
    encontrado = False

    for d in data:
        if int(d["id"]) == id and d["estado"] == "activo":
            d["nombre"] = nuevo["nombre"]
            d["genero"] = nuevo["genero"]
            d["nivel_emocional"] = nuevo["nivel_emocional"]
            encontrado = True
            break

    if not encontrado:
        return None

    save_kdramas(data)
    return nuevo


def delete_kdrama(id):
    data = read_kdramas()
    encontrado = False

    for d in data:
        if int(d["id"]) == id:
            d["estado"] = "inactivo"
            encontrado = True
            break

    if not encontrado:
        return False

    save_kdramas(data)
    return True


# =============================
# PERSONALIDAD
# =============================

def read_personalidad():
    try:
        with open(PERSONALIDAD_FILE, "r", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def save_personalidad(data):
    with open(PERSONALIDAD_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "id_usuario", "romantico", "aventurero", "oscuro", "intenso", "estado"]
        )
        writer.writeheader()
        writer.writerows(data)


def create_personalidad(p):
    p["id"] = generar_id(PERSONALIDAD_FILE)
    p["estado"] = "activo"

    data = read_personalidad()
    data.append(p)
    save_personalidad(data)

    return p


def get_personalidades():
    data = read_personalidad()
    return [p for p in data if p.get("estado") == "activo"]


def update_personalidad(id, nuevo):
    data = read_personalidad()
    encontrado = False

    for p in data:
        if int(p["id"]) == id and p["estado"] == "activo":
            p["id_usuario"] = nuevo["id_usuario"]
            p["romantico"] = nuevo["romantico"]
            p["aventurero"] = nuevo["aventurero"]
            p["oscuro"] = nuevo["oscuro"]
            p["intenso"] = nuevo["intenso"]
            encontrado = True
            break

    if not encontrado:
        return None

    save_personalidad(data)
    return nuevo


def delete_personalidad(id):
    data = read_personalidad()
    encontrado = False

    for p in data:
        if int(p["id"]) == id:
            p["estado"] = "inactivo"
            encontrado = True
            break

    if not encontrado:
        return False

    save_personalidad(data)
    return True