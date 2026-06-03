from sqlmodel import Session, select
from src.database import engine
from src.models.models import KDrama

def create_kdrama(drama_data: dict):
    with Session(engine) as session:
        drama = KDrama(**drama_data)
        session.add(drama)
        session.commit()
        session.refresh(drama)
        return drama.model_dump()


def get_kdramas():
    with Session(engine) as session:
        statement = select(KDrama)
        return [k.model_dump() for k in session.exec(statement).all()]


def update_kdrama(id, nuevo: dict):
    with Session(engine) as session:
        drama = session.get(KDrama, id)
        if not drama:
            return None
        drama.nombre = nuevo["nombre"]
        drama.genero = nuevo["genero"]
        drama.nivel_emocional = nuevo["nivel_emocional"]
        drama.descripcion = nuevo.get("descripcion", drama.descripcion)
        drama.imagen_url = nuevo.get("imagen_url", drama.imagen_url)
        session.add(drama)
        session.commit()
        session.refresh(drama)
        return drama.model_dump()


def delete_kdrama(id):
    with Session(engine) as session:
        drama = session.get(KDrama, id)
        if not drama:
            return False
        session.delete(drama)
        session.commit()
        return True
