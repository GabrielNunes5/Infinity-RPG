from models.database import SessionLocal
from models.character import Character
from views.login import user_session


class CreateCharacterController:
    def __init__(self, page, update_view):
        self.page = page
        self.update_view = update_view
        self.classes = [
            {"name": "Bárbaro", "image": "assets/barbaro.png"},
            {"name": "Bardo", "image": "assets/bardo.png"},
            {"name": "Bruxo", "image": "assets/bruxo.png"},
            {"name": "Caçador", "image": "assets/caçador.png"},
            {"name": "Druida", "image": "assets/druida.png"},
            {"name": "Feiticeiro", "image": "assets/feiticeiro.png"},
            {"name": "Guerreiro", "image": "assets/guerreiro.png"},
            {"name": "Ladino", "image": "assets/ladino.png"},
            {"name": "Mago", "image": "assets/mago.png"},
            {"name": "Monge", "image": "assets/monge.png"},
            {"name": "Paladino", "image": "assets/paladino.png"},
            {"name": "Sacerdote", "image": "assets/sacerdote.png"},
        ]
        self.current_class_index = 0

    @property
    def class_image(self):
        return self.classes[self.current_class_index]["image"]

    @property
    def class_name(self):
        return self.classes[self.current_class_index]["name"]

    def next_class(self, e):
        self.current_class_index = (
            self.current_class_index + 1) % len(self.classes)
        self.update_view()

    def previous_class(self, e):
        self.current_class_index = (
            self.current_class_index - 1) % len(self.classes)
        self.update_view()

    def save_character(self, character_data):
        # Criar uma nova sessão do banco de dados
        session = SessionLocal()
        try:
            # Cria uma instância de Character
            new_character = Character(
                user_id=user_session.get("user_id"),
                name=character_data["name"],
                clas=character_data["class"],
                class_image=self.class_image,
                race=character_data["race"],
                strength=character_data["attributes"]
                ["Força"],
                dexterity=character_data["attributes"]
                ["Destreza"],
                constitution=character_data["attributes"]
                ["Constituição"],
                intelligence=character_data["attributes"]
                ["Inteligência"],
                wisdom=character_data["attributes"]
                ["Sabedoria"],
                charisma=character_data["attributes"]
                ["Carisma"],
                skin_color=character_data["skin_color"],
                hair=character_data["hair_color"]
            )
            # Adiciona e confirma a transação
            session.add(new_character)
            session.commit()

            print("Personagem criado com sucesso!")
        except Exception as e:
            session.rollback()
            print(f"Erro ao salvar o personagem: {e}")
        finally:
            session.close()

    def load_character(self, character_data):
        self.character_data = character_data
        self.current_class_index = next(
            (i for i,
             cls in enumerate(
                 self.classes) if cls["name"] == character_data["class"]), 0)

    def update_character(self, character_id, character_data):
        session = SessionLocal()
        try:
            character = session.query(Character).filter(
                Character.id == character_id).first()
            if character:
                character.name = character_data["name"]
                character.clas = character_data["class"]
                character.class_image = character_data["class_image"]
                character.race = character_data["race"]
                character.strength = character_data["attributes"]
                ["Força"]
                character.dexterity = character_data["attributes"]
                ["Destreza"]
                character.constitution = character_data["attributes"]
                ["Constituição"]
                character.intelligence = character_data["attributes"]
                ["Inteligência"]
                character.wisdom = character_data["attributes"]
                ["Sabedoria"]
                character.charisma = character_data["attributes"]
                ["Carisma"]
                character.skin_color = character_data["skin_color"]
                character.hair = character_data["hair_color"]
                session.commit()
        finally:
            session.close()
