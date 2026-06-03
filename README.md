# K-Drama Hub

Plataforma web para explorar, descubrir y recibir recomendaciones personalizadas de K-Dramas según la personalidad del usuario.

---

## Descripción

K-Drama Hub es una aplicación full-stack que permite a los usuarios navegar un catálogo de K-Dramas, filtrarlos por género, ver su nivel emocional y obtener recomendaciones basadas en su perfil de personalidad. Cuenta con un sistema de autenticación con roles diferenciados (usuario y administrador).

---

## Tecnologías utilizadas

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3 · FastAPI · SQLModel · SQLAlchemy |
| Base de datos | PostgreSQL (Neon serverless) |
| Autenticación | JWT (python-jose) · bcrypt (passlib) |
| Frontend | HTML · CSS · JavaScript vanilla |
| Servidor | Uvicorn |

---

## Estructura del proyecto

```
Proyecto-desarrollo-S-main/
├── frontend/
│   ├── css/
│   │   └── styles.css
│   ├── index.html          # Catálogo principal de K-Dramas
│   ├── login.html          # Inicio de sesión y registro
│   ├── perfil.html         # Perfil y personalidad del usuario
│   ├── estadisticas.html   # Estadísticas del catálogo
│   └── admin.html          # Panel de administración
├── src/
│   ├── main.py             # Aplicación FastAPI y definición de rutas
│   ├── database.py         # Configuración del motor de base de datos
│   ├── models/
│   │   ├── models.py       # Modelos: Usuario, KDrama, Personalidad
│   │   └── genero.py       # Enum de géneros disponibles
│   └── operations/
│       ├── kdrama_operations.py
│       ├── usuario_operations.py
│       └── personalidad_operations.py
├── init/
├── test/
│   └── test_main.http      # Pruebas de endpoints HTTP
├── .env                    # Variables de entorno (no subir al repo)
├── requirements.txt
└── README.md
```

---

## Arquitectura del sistema

El sistema está organizado en tres capas:

```
┌─────────────────────────────────────────────────────┐
│                   CAPA CLIENTE                      │
│   index.html · login.html · perfil.html             │
│   estadisticas.html · admin.html                    │
│         HTML + CSS + JavaScript vanilla             │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / JWT
┌──────────────────────▼──────────────────────────────┐
│                  CAPA SERVIDOR                      │
│                FastAPI + Uvicorn                    │
│  ┌────────────┐ ┌───────────┐ ┌──────────────────┐  │
│  │   Auth     │ │ Rutas API │ │   Operations     │  │
│  │ JWT·bcrypt │ │/kdramas   │ │ CRUD + negocio   │  │
│  └────────────┘ │/usuarios  │ └──────────────────┘  │
│  ┌────────────┐ │/personal. │ ┌──────────────────┐  │
│  │  Modelos   │ │/recomendar│ │  Recomendador    │  │
│  │ SQLModel   │ └───────────┘ │ Personalidad →   │  │
│  │ Pydantic   │               │ géneros          │  │
│  └────────────┘               └──────────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │ SQLAlchemy · SSL
┌──────────────────────▼──────────────────────────────┐
│               CAPA DE DATOS                         │
│         PostgreSQL en Neon (remoto)                 │
│   tabla usuario · tabla kdrama · tabla personalidad │
└─────────────────────────────────────────────────────┘
```

---

## Diagrama Entidad-Relación

```mermaid
erDiagram
    USUARIO ||--o{ PERSONALIDAD : "tiene"

    USUARIO {
        int id PK
        string nombre
        int edad
        string email
        string password
        string rol
    }

    PERSONALIDAD {
        int id PK
        int id_usuario FK
        bool romantico
        bool aventurero
        bool sensible
        bool extrovertido
        bool oscuro
        bool intenso
    }

    KDRAMA {
        int id PK
        string nombre
        string genero
        int nivel_emocional
        string descripcion
        string imagen_url
    }
```

> **Relación principal:** Un `USUARIO` puede tener cero o una `PERSONALIDAD` (1:N). El módulo de recomendaciones cruza `PERSONALIDAD` con `KDRAMA` en tiempo de ejecución, sin tabla intermedia.

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git https://github.com/Mafe68249/Proyecto-desarrollo-S.git
cd tu-repositorio
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
DATABASE_URL=postgresql://usuario:contraseña@host/base_de_datos?sslmode=require
```

> ️ Nunca subas el archivo `.env` al repositorio. Asegúrate de que esté incluido en `.gitignore`.

### 5. Ejecutar la aplicación

```bash
uvicorn src.main:app --reload
```

La aplicación estará disponible en `http://localhost:8000`.

---

## Modelos de datos

### Usuario
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | int | Clave primaria |
| nombre | str | Mínimo 2 caracteres |
| edad | int | Mayor a 0 |
| email | str | Único, indexado |
| password | str | Mínimo 4 caracteres (almacenado con hash) |
| rol | str | `"usuario"` o `"admin"` |

### KDrama
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | int | Clave primaria |
| nombre | str | Título del K-Drama |
| genero | Genero | Enum: romance, accion, comedia, terror, suspenso, drama |
| nivel_emocional | int | Escala del 1 al 10 |
| descripcion | str (opcional) | Sinopsis |
| imagen_url | str (opcional) | URL de la imagen de portada |

### Personalidad
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | int | Clave primaria |
| id_usuario | int | FK → Usuario |
| romantico | bool | |
| aventurero | bool | |
| sensible | bool | |
| extrovertido | bool | |
| oscuro | bool | |
| intenso | bool | |

---

## Endpoints de la API

La documentación interactiva está disponible en `http://localhost:8000/docs`.

### Autenticación

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/registro` | Registrar nuevo usuario |
| POST | `/login` | Iniciar sesión, retorna JWT |
| GET | `/usuarios/me` | Obtener usuario autenticado |

### K-Dramas

| Método | Ruta | Acceso | Descripción |
|--------|------|--------|-------------|
| GET | `/kdramas` | Público | Listar todos los K-Dramas |
| GET | `/kdramas/{id}` | Público | Obtener K-Drama por ID |
| GET | `/kdramas/buscar/{nombre}` | Público | Buscar por nombre |
| GET | `/kdramas/genero/{genero}` | Público | Filtrar por género |
| POST | `/kdramas` | Admin | Crear K-Drama |
| PUT | `/kdramas/{id}` | Admin | Actualizar K-Drama |
| DELETE | `/kdramas/{id}` | Admin | Eliminar K-Drama |

### Usuarios

| Método | Ruta | Acceso | Descripción |
|--------|------|--------|-------------|
| GET | `/usuarios` | Público | Listar usuarios |
| GET | `/usuarios/{id}` | Público | Obtener usuario por ID |
| GET | `/usuarios/buscar/{nombre}` | Público | Buscar por nombre |
| POST | `/usuarios` | Admin | Crear usuario |
| PUT | `/usuarios/{id}` | Admin | Actualizar usuario |
| DELETE | `/usuarios/{id}` | Admin | Eliminar usuario |

### Personalidad

| Método | Ruta | Acceso | Descripción |
|--------|------|--------|-------------|
| GET | `/personalidad/mi-personalidad` | Autenticado | Ver mi personalidad |
| POST | `/personalidad/mi-personalidad` | Autenticado | Crear o actualizar mi personalidad |
| GET | `/personalidad` | Público | Listar personalidades |
| GET | `/personalidad/{id}` | Público | Obtener personalidad por ID |
| POST | `/personalidad` | Admin | Crear personalidad |
| PUT | `/personalidad/{id}` | Admin | Actualizar personalidad |
| DELETE | `/personalidad/{id}` | Admin | Eliminar personalidad |

### Recomendaciones

| Método | Ruta | Acceso | Descripción |
|--------|------|--------|-------------|
| GET | `/recomendar/mis-recomendaciones` | Autenticado | Recomendaciones para el usuario logueado |
| GET | `/recomendar/{id_usuario}` | Público | Recomendaciones por ID de usuario |

---

## Lógica de recomendación

El sistema cruza la personalidad del usuario con el catálogo de K-Dramas según estas reglas:

- **Romántico** → K-Dramas de género *romance*
- **Aventurero** → K-Dramas de género *acción*
- **Oscuro** → K-Dramas de género *terror* o *suspenso*
- **Intenso** → K-Dramas con nivel emocional ≥ 8

---

## Autenticación

La API usa **JWT (JSON Web Tokens)**. Para acceder a los endpoints protegidos:

1. Realiza un `POST /login` con tu email y contraseña.
2. Copia el campo `access_token` de la respuesta.
3. Incluye el token en el header de tus peticiones:
   ```
   Authorization: Bearer <tu_token>
   ```

Los tokens tienen una validez de **24 horas**.

---

## Roles

| Rol | Permisos |
|-----|----------|
| `usuario` | Ver catálogo, gestionar su propia personalidad, obtener recomendaciones |
| `admin` | Todo lo anterior + crear, editar y eliminar K-Dramas, usuarios y personalidades |

---

## Pruebas

El archivo `test/test_main.http` contiene ejemplos de peticiones HTTP para probar los endpoints directamente desde IDEs como VS Code (con la extensión REST Client) o IntelliJ.

---

## Notas importantes

- El archivo `.env` **no debe subirse** al repositorio. Agrega `.env` a tu `.gitignore`.
- La `SECRET_KEY` usada para firmar los JWT en `main.py` debe cambiarse por una clave segura antes de desplegar en producción.
- La base de datos utilizada es **PostgreSQL en Neon** (serverless). Puedes usar cualquier instancia de PostgreSQL cambiando la variable `DATABASE_URL`.

---

## Autores

Proyecto desarrollado como parte del curso de **Desarrollo de Software**.
