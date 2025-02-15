import flet as ft
from controllers.create_character_controller import CreateCharacterController
from config import DND_RACES, atribute_configs, HAIR_COLORS, SKIN_COLORS
from models.database import SessionLocal
from models.character import Character


def create_character_view(page: ft.Page, character_id=None):
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

    # Texto para redirecionar para a página de personagens
    character_redirect_text = ft.TextButton(
        "Voltar para Página de Personagens",
        on_click=lambda _: page.go("/characters"))

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

    # Dropdown da cor de cabelo
    hair_color_dropdown = generate_color_dropdown(
        HAIR_COLORS, "Cor do Cabelo")

    # Dropdown da cor da pele
    skin_color_dropdown = generate_color_dropdown(
        SKIN_COLORS, "Cor da Pele")

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
                                     **atribute_configs),
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
            "class_image": controller.class_image,
            "race": race_dropdown.value,
            "hair_color": hair_color_dropdown.value,
            "skin_color": skin_color_dropdown.value,
            "attributes": {k:
                           int(v.value) for k, v in attribute_fields.items()}
        }
        controller.update_character(character_id, character_data)
        if not character_id:
            controller.save_character(character_data)
        page.go('/characters')

    # Botão de instruções
    def show_instructions(e):
        instructions_dialog.open = True
        page.update()

    instructions_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Instruções de preenchimento",
                      size=22, weight=ft.FontWeight.W_700),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Complete os campos corretamente.",
                        size=18,
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Text("Crie o nome de personagem único."),
                    ft.Text("Selecione a classe do seu personagem."),
                    ft.Text("Os atributos devem estar entre 8 e 20."),
                    ft.Text("Força: Força física e combate."),
                    ft.Text("Constituição: Resistência a dano e resiliência."),
                    ft.Text("Destreza: Agilidade e precisão."),
                    ft.Text("Inteligência: Capacidade de aprendizado."),
                    ft.Text("Sabedoria: Percepção e intuição."),
                    ft.Text("Carisma: Persuasão e liderança."),
                    ft.Text("Selecione a raça, cor do cabelo e cor da pele."),
                    ft.Text("Clique em 'Criar Novo Personagem' para salvar."),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=8,
            ),
            width=500,
            height=400,
            padding=10,
            border_radius=8,
        ),
        actions=[
            ft.TextButton(
                "Fechar",
                on_click=lambda _: page.close(instructions_dialog),
            ),
        ],
    )

    # Botões de navegação para trocar a imagem da classe
    navigation_buttons = ft.Row(
        [
            ft.IconButton(icon=ft.Icons.ARROW_BACK,
                          on_click=controller.previous_class),
            ft.IconButton(icon=ft.Icons.ARROW_FORWARD,
                          on_click=controller.next_class)
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Botão para criar personagem
    create_character_button = ft.ElevatedButton(
        bgcolor="#000000",
        color="#FFFFFF",
        width=210,
        height=20,
        text="Criar Novo Personagem",
        on_click=create_character)

    # Verifica se está no modo de edição
    if character_id:
        session = SessionLocal()
        try:
            # Busca os dados do personagem no banco de dados
            character = session.query(Character).filter(
                Character.id == character_id).first()
            if character:
                character_name_field.value = character.name
                class_image.src = character.class_image
                class_name_field.value = character.clas
                race_dropdown.value = character.race
                skin_color_dropdown.value = character.skin_color
                hair_color_dropdown.value = character.hair
                attribute_fields["Força"].value = str(character.strength)
                attribute_fields["Constituição"].value = str(
                    character.constitution)
                attribute_fields["Destreza"].value = str(character.dexterity)
                attribute_fields["Inteligência"].value = str(
                    character.intelligence)
                attribute_fields["Sabedoria"].value = str(character.wisdom)
                attribute_fields["Carisma"].value = str(character.charisma)
                create_character_button.text = "Salvar Personagem"
        finally:
            session.close()

    # Estrutura da página
    create_character_page = ft.View(
        "/create_character",
        [
            ft.Row(
                controls=[
                    ft.Container(
                        bgcolor="#212121",
                        width=800,
                        height=700,
                        border_radius=35,
                        padding=10,
                        content=ft.Column(
                            controls=[
                                character_name_field,
                                class_image,
                                navigation_buttons,
                                ft.Row(
                                    [
                                        class_name_field,
                                        ft.IconButton(
                                            icon=ft.Icons.HELP,
                                            on_click=show_instructions
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
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
                                create_character_button,
                                character_redirect_text,
                                instructions_dialog
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        ]
    )

    return create_character_page
