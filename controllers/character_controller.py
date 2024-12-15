from models.database import SessionLocal
from models.character import Character
from views.login import user_session


def load_characters():
    # Carrega os personagens do usuário logado.
    session = SessionLocal()
    user_id = user_session.get("user_id")
    if not user_id:
        session.close()
        return None, []  # Nenhum usuário logado
    characters = session.query(Character).filter_by(user_id=user_id).all()
    session.close()
    return user_id, characters


def delete_character(char_id):
    # Deleta um personagem pelo ID.
    session = SessionLocal()
    character = session.query(Character).get(char_id)
    if character:
        session.delete(character)
        session.commit()
    session.close()


def prepare_character_for_edit(char_id, page):
    # Prepara o personagem para edição.
    page.session.set("character_to_edit", char_id)
