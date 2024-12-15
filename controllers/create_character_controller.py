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
        print("Personagem criado com sucesso!")
        print(character_data)
