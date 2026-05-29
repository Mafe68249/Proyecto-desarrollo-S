from sqlmodel import Session, select
from src.database import engine
from src.models.models import Personalidad

def create_personalidad(personalidad):

    with Session(engine) as session:
        session.add(personalidad)
        session.commit()
        session.refresh(personalidad)

        return personalidad


def get_personalidades():

    with Session(engine) as session:
        statement = select(Personalidad)
        return session.exec(statement).all()


def update_personalidad(id, nuevo):

    with Session(engine) as session:

        personalidad = session.get(Personalidad, id)

        if not personalidad:
            return None

        personalidad.id_usuario = nuevo.id_usuario
        personalidad.romantico = nuevo.romantico
        personalidad.aventurero = nuevo.aventurero
        personalidad.sensible = nuevo.sensible
        personalidad.extrovertido = nuevo.extrovertido
        personalidad.oscuro = nuevo.oscuro
        personalidad.intenso = nuevo.intenso

        session.add(personalidad)
        session.commit()
        session.refresh(personalidad)

        return personalidad


def delete_personalidad(id):

    with Session(engine) as session:

        personalidad = session.get(Personalidad, id)

        if not personalidad:
            return False

        session.delete(personalidad)
        session.commit()

        return True