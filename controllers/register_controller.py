from models.database import SessionLocal
from models.user import User
import re
from config import hash_password


class UserController:
    @staticmethod
    def validade_user_data(name, username, email, password):
        errors = []

        # Validar nome
        if not name or len(name.split()) < 2:
            errors.append("Nome completo é obrigatorio!")

        # Validar nome de usuario
        if not username or len(username) < 3:
            errors.append("Usuário precisa ter pelo menos 3 caracteres!")

        # Validar email
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            errors.append('Email invalido')

        # Validar senha
        if len(password) < 12:
            errors.append('Senha precisa ter pelo menos 12 caracteres!')
        if not any(char.isupper() for char in password):
            errors.append('Senha precisa ter ao menos uma letra maiuscula!')
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in password):
            errors.append('Senha precisa ter ao menos um caractere especial!')

        # Sessão para verificar unicidade
        session = SessionLocal()
        try:
            if session.query(User).filter_by(username=username).first():
                errors.append("Usuário já existe.")
            if session.query(User).filter_by(email=email).first():
                errors.append("Email já cadastrado.")
        finally:
            session.close()

        return errors

    @staticmethod
    def register_user(name, username, email, password):
        session = SessionLocal()
        user = User(
            name=name,
            username=username,
            email=email,
            password=hash_password(password)
        )

        try:
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)
        finally:
            session.close()

        return None
