class CreateCharacterController:
    def __init__(self, page, update_view):
        self.page = page
        self.update_view = update_view
        self.classes = [
            {"name": "Bárbaro", "image": "/images/barbaro.png"},
            {"name": "Mago", "image": "/images/mago.png"},
            {"name": "Ladino", "image": "/images/ladino.png"}
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
