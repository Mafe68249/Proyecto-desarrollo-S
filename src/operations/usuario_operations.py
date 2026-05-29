from sqlmodel import Session, select
from src.database import engine
from src.models.models import Usuario

def create_usuario(usuario):

    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)

        return usuario


def get_usuarios():

    with Session(engine) as session:
        statement = select(Usuario)
        return session.exec(statement).all()


def update_usuario(id, nuevo):

    with Session(engine) as session:

        usuario = session.get(Usuario, id)

        if not usuario:
            return None

        usuario.nombre = nuevo.nombre
        usuario.edad = nuevo.edad

        session.add(usuario)
        session.commit()
        session.refresh(usuario)

        return usuario


def delete_usuario(id):

    with Session(engine) as session:

        usuario = session.get(Usuario, id)

        if not usuario:
            return False

        session.delete(usuario)
        session.commit()

        return True

