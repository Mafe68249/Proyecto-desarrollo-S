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


# -----------------------------
# USUARIOS
# -----------------------------

def create_usuario(usuario):
    usuario["id"] = generar_id(USUARIOS_FILE)
    usuario["estado"] = "activo"

    file_exists = os.path.isfile(USUARIOS_FILE)

    with open(USUARIOS_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=usuario.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(usuario)

    return usuario


def get_usuarios():
    try:
        with open(USUARIOS_FILE, mode="r", encoding="utf-8") as file:
            data = list(csv.DictReader(file))
            return [u for u in data if u.get("estado", "activo") == "activo"]
    except FileNotFoundError:
        return []


def get_usuarios_all():
    try:
        with open(USUARIOS_FILE, mode="r", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def update_usuario(id, nuevo_usuario):
    usuarios = get_usuarios_all()
    actualizado = False

    for u in usuarios:
        if int(u["id"]) == id and u["estado"] == "activo":
            u["nombre"] = nuevo_usuario["nombre"]
            u["edad"] = nuevo_usuario["edad"]
            actualizado = True
            break

    if not actualizado:
        return None

    with open(USUARIOS_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=usuarios[0].keys())
        writer.writeheader()
        writer.writerows(usuarios)

    return nuevo_usuario


def delete_usuario(id):
    usuarios = get_usuarios_all()
    eliminado = False

    for u in usuarios:
        if int(u["id"]) == id:
            u["estado"] = "inactivo"
            eliminado = True
            break

    if not eliminado:
        return False

    with open(USUARIOS_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=usuarios[0].keys())
        writer.writeheader()
        writer.writerows(usuarios)

    return True


# -----------------------------
# K-DRAMAS
# -----------------------------

def create_kdrama(drama):
    drama["id"] = generar_id(KDRAMAS_FILE)
    drama["estado"] = "activo"

    file_exists = os.path.isfile(KDRAMAS_FILE)

    with open(KDRAMAS_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=drama.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(drama)

    return drama


def get_kdramas():
    try:
        with open(KDRAMAS_FILE, mode="r", encoding="utf-8") as file:
            data = list(csv.DictReader(file))
            return [d for d in data if d.get("estado", "activo") == "activo"]
    except FileNotFoundError:
        return []


def get_kdramas_all():
    try:
        with open(KDRAMAS_FILE, mode="r", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def update_kdrama(id, nuevo):
    dramas = get_kdramas_all()
    actualizado = False

    for d in dramas:
        if int(d["id"]) == id and d["estado"] == "activo":
            d["nombre"] = nuevo["nombre"]
            d["genero"] = nuevo["genero"]
            d["nivel_emocional"] = nuevo["nivel_emocional"]
            actualizado = True
            break

    if not actualizado:
        return None

    with open(KDRAMAS_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=dramas[0].keys())
        writer.writeheader()
        writer.writerows(dramas)

    return nuevo


def delete_kdrama(id):
    dramas = get_kdramas_all()
    eliminado = False

    for d in dramas:
        if int(d["id"]) == id:
            d["estado"] = "inactivo"
            eliminado = True
            break

    if not eliminado:
        return False

    with open(KDRAMAS_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=dramas[0].keys())
        writer.writeheader()
        writer.writerows(dramas)

    return True


# -----------------------------
# PERSONALIDAD
# -----------------------------

def create_personalidad(p):
    p["id"] = generar_id(PERSONALIDAD_FILE)
    p["estado"] = "activo"

    file_exists = os.path.isfile(PERSONALIDAD_FILE)

    with open(PERSONALIDAD_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=p.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(p)

    return p


def get_personalidades():
    try:
        with open(PERSONALIDAD_FILE, mode="r", encoding="utf-8") as file:
            data = list(csv.DictReader(file))
            return [p for p in data if p.get("estado", "activo") == "activo"]
    except FileNotFoundError:
        return []


def get_personalidades_all():
    try:
        with open(PERSONALIDAD_FILE, mode="r", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def get_personalidad_by_id(id):
    data = get_personalidades_all()

    for p in data:
        if int(p["id"]) == id:
            return p

    return None


def update_personalidad(id, nuevo):
    data = get_personalidades_all()
    actualizado = False

    for p in data:
        if int(p["id"]) == id and p["estado"] == "activo":
            p["id_usuario"] = nuevo["id_usuario"]
            p["romantico"] = nuevo["romantico"]
            p["aventurero"] = nuevo["aventurero"]
            p["oscuro"] = nuevo["oscuro"]
            p["intenso"] = nuevo["intenso"]
            actualizado = True
            break

    if not actualizado:
        return None

    with open(PERSONALIDAD_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    return nuevo


def delete_personalidad(id):
    data = get_personalidades_all()
    eliminado = False

    for p in data:
        if int(p["id"]) == id:
            p["estado"] = "inactivo"
            eliminado = True
            break

    if not eliminado:
        return False

    with open(PERSONALIDAD_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    return True