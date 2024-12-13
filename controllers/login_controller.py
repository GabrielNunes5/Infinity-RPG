from models.database import SessionLocal
from models.user import User
from bcrypt import checkpw


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
