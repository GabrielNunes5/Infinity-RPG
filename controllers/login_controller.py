from models.database import SessionLocal
from models.user import User
from bcrypt import checkpw, hashpw, gensalt


class LoginController:
    @staticmethod
    def authenticate_user(username: str, password: str) -> dict:
        """Autentica o usuário com base no username e senha."""
        session = SessionLocal()
        user = session.query(User).filter_by(username=username).first()
        session.close()

        if user and checkpw(password.encode(), user.password.encode()):
            return {"status": True,
                    "user_id": user.id,
                    "username": user.username}
        else:
            return {"status": False,
                    "message": "Credenciais inválidas"}

    @staticmethod
    def verify_user_and_email(username: str, email: str) -> dict:
        """Verifica se o usuário e o e-mail existem no banco de dados."""
        session = SessionLocal()
        user = session.query(User).filter_by(
            username=username, email=email).first()
        session.close()

        if user:
            return {"status": True}
        else:
            return {"status": False,
                    "message": "Usuário ou e-mail não cadastrado"}

    @staticmethod
    def update_password(username: str, new_password: str) -> dict:
        """Atualiza a senha de um usuário no banco de dados."""
        session = SessionLocal()
        user = session.query(User).filter_by(username=username).first()

        if user:
            # Hash da nova senha
            hashed_password = hashpw(new_password.encode(), gensalt())
            user.password = hashed_password.decode()
            session.commit()
            session.close()
            return {"status": True, "message": "Senha atualizada com sucesso"}
        else:
            session.close()
            return {"status": False, "message": "Usuário não encontrado"}
