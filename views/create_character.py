import flet as ft
from controllers.create_character_controller import CreateCharacterController
from config import HAIR_AND_SKIN_COLORS
from config import DND_RACES, atribute_configs


def create_character_view(page: ft.Page):
    # Declara como None inicialmente para evitar problemas de escopo
    controller = None

    # Função de atualização da view
    def update_view():
        class_image.src = controller.class_image
        class_name_field.value = controller.class_name
        page.update()

    controller = CreateCharacterController(page, update_view)

    # Input do nome do personagem
    character_name_field = ft.TextField(label="Nome do Personagem", width=300)

    # Imagem e classe
    class_image = ft.Image(src=controller.class_image, width=150, height=150)
    class_name_field = ft.Text(
        value=controller.class_name, size=18, color="#FFFFFF")

    # Dropdowns de Raça
    race_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(race) for race in DND_RACES],
        label="Raça",
        width=200
    )

    # Função para gerar opções com círculos coloridos
    def generate_color_dropdown(options, label):
        return ft.Dropdown(
            options=[
                ft.dropdown.Option(
                    content=ft.Row(
                        [
                            ft.Container(
                                width=15,
                                height=15,
                                border_radius=15,
                                bgcolor=color["hex"],
                                margin=ft.margin.only(right=10)
                            ),
                            ft.Text(color["name"], size=12, color="white")
                        ]
                    ),
                    key=color["name"]
                ) for color in options
            ],
            label=label,
            width=200
        )

    hair_color_dropdown = generate_color_dropdown(
        HAIR_AND_SKIN_COLORS, "Cor do Cabelo")

    skin_color_dropdown = generate_color_dropdown(
        HAIR_AND_SKIN_COLORS, "Cor da Pele")

    # Validação dos atributos
    def validate_input(e):
        try:
            value = int(e.control.value)
            if value < 8 or value > 20:
                e.control.value = "8"
                e.control.update()
        except ValueError:
            e.control.value = "8"
            e.control.update()

    # Campos de atributos
    attribute_fields = {
        "Força": ft.TextField(label="Força",
                              on_blur=validate_input,
                              **atribute_configs),
        "Constituição": ft.TextField(label="Constituição",
                                     on_blur=validate_input,
                                     **atribute_configs
                                     ),
        "Destreza": ft.TextField(label="Destreza",
                                 on_blur=validate_input,
                                 **atribute_configs),
        "Inteligência": ft.TextField(label="Inteligência",
                                     on_blur=validate_input,
                                     **atribute_configs),
        "Sabedoria": ft.TextField(label="Sabedoria",
                                  on_blur=validate_input,
                                  **atribute_configs),
        "Carisma": ft.TextField(label="Carisma",
                                on_blur=validate_input,
                                **atribute_configs),
    }

    # Função para criar o personagem
    def create_character(e):
        if not all([
            character_name_field.value,
            race_dropdown.value,
            hair_color_dropdown.value,
            skin_color_dropdown.value
        ]):
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    "Por favor, preencha todos os campos!", color="white"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        character_data = {
            "name": character_name_field.value,
            "class": controller.class_name,
            "race": race_dropdown.value,
            "hair_color": hair_color_dropdown.value,
            "skin_color": skin_color_dropdown.value,
            "attributes": {k: int(
                v.value) for k, v in attribute_fields.items()}
        }
        controller.save_character(character_data)

    # Botões de navegação para trocar a imagem da classe
    navigation_buttons = ft.Row(
        [
            ft.IconButton(icon=ft.icons.ARROW_BACK,
                          on_click=controller.previous_class),
            ft.IconButton(icon=ft.icons.ARROW_FORWARD,
                          on_click=controller.next_class)
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Botão para criar personagem
    create_character_button = ft.ElevatedButton(
        bgcolor="#000000",
        color="#FFFFFF",
        width=210,
        height=25,
        text="Criar Novo Personagem",
        on_click=create_character)

    # Layout dentro do Container principal
    main_container = ft.Container(
        bgcolor="#212121",
        width=800,
        height=680,
        border_radius=35,
        padding=20,
        content=ft.Column(
            controls=[
                character_name_field,
                class_image,
                navigation_buttons,
                class_name_field,
                ft.Row(
                    [
                        attribute_fields["Força"],
                        attribute_fields["Destreza"],
                        attribute_fields["Inteligência"]
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        attribute_fields["Constituição"],
                        attribute_fields["Sabedoria"],
                        attribute_fields["Carisma"]
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                race_dropdown,
                hair_color_dropdown,
                skin_color_dropdown,
                create_character_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # Row principal que segura o container
    create_character_view = ft.View(
        route="/create_character",
        controls=[
            ft.Row(
                controls=[main_container],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        bgcolor="#000000"
    )

    return create_character_view
