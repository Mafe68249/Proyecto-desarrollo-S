from pydantic import SQLModel, Field
from src.models.genero import Genero
from typing import Optional

class Usuario(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2)
    edad: int = Field(gt=0)


class Personalidad(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    id_usuario: int = Field(foreign_key="usuario.id")

    romantico: bool
    aventurero: bool
    sensible: bool
    extrovertido: bool
    oscuro: bool
    intenso: bool


class KDrama(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    nombre: str
    genero: Genero
    nivel_emocional: int

