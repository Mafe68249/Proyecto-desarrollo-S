from sqlmodel import Session, select
from src.database import engine
from src.models.models import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_usuario(usuario_data: dict):
    with Session(engine) as session:
        if "password" in usuario_data:
            usuario_data["password"] = hash_password(usuario_data["password"])
        usuario = Usuario(**usuario_data)
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        usuario_dict = usuario.model_dump()
        usuario_dict.pop("password", None)
        return usuario_dict

def get_usuarios():
    with Session(engine) as session:
        statement = select(Usuario)
        usuarios = session.exec(statement).all()
        return [{k: v for k, v in u.model_dump().items() if k != "password"} for u in usuarios]


def get_usuario_by_email(email: str):
    from src.database import engine
    from src.models.models import Usuario
    from sqlmodel import Session, select

    with Session(engine) as session:
        statement = select(Usuario).where(Usuario.email == email)
        return session.exec(statement).first()

def update_usuario(id, nuevo_data):
    with Session(engine) as session:
        usuario = session.get(Usuario, id)
        if not usuario:
            return None
        for key, value in nuevo_data.items():
            if key == "password" and value:
                setattr(usuario, key, hash_password(value))
            elif key != "password":
                setattr(usuario, key, value)
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        usuario_dict = usuario.model_dump()
        usuario_dict.pop("password", None)
        return usuario_dict

def delete_usuario(id):
    with Session(engine) as session:
        usuario = session.get(Usuario, id)
        if not usuario:
            return False
        session.delete(usuario)
        session.commit()
        return True