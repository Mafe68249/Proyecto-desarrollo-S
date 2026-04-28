from enum import Enum

class Genero(str, Enum):
    romance = "romance"
    accion = "accion"
    comedia = "comedia"
    terror = "terror"
    suspenso = "suspenso"
    drama = "drama"