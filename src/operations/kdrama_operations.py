from sqlmodel import Session, select
from src.database import engine
from src.models.models import KDrama

def create_kdrama(drama):

    with Session(engine) as session:
        session.add(drama)
        session.commit()
        session.refresh(drama)

        return drama


def get_kdramas():

    with Session(engine) as session:
        statement = select(KDrama)
        return session.exec(statement).all()


def update_kdrama(id, nuevo):

    with Session(engine) as session:

        drama = session.get(KDrama, id)

        if not drama:
            return None

        drama.nombre = nuevo.nombre
        drama.genero = nuevo.genero
        drama.nivel_emocional = nuevo.nivel_emocional

        session.add(drama)
        session.commit()
        session.refresh(drama)

        return drama


def delete_kdrama(id):

    with Session(engine) as session:

        drama = session.get(KDrama, id)

        if not drama:
            return False

        session.delete(drama)
        session.commit()

        return True