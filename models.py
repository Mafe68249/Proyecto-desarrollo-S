from pydantic import BaseModel, Field
from genero import Genero




class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2)
    edad: int = Field(..., gt=0)


class Personalidad(BaseModel):
    id_usuario: int
    romantico: bool
    aventurero: bool
    sensible: bool
    extrovertido: bool
    oscuro: bool
    intenso: bool


class KDrama(BaseModel):
    nombre: str
    genero: Genero
    nivel_emocional: int = Field(..., ge=1, le=10)



class Usuarioid(Usuario):
    id: int = Field(...)


class KDramaid(KDrama):
    id: int = Field(...)