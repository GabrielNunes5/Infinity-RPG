import flet as ft
from controllers.character_controller import (
    load_characters, delete_character, prepare_character_for_edit)


def character_view(page: ft.Page):
    # Carrega os personagens do usuário logado
    user_id, characters = load_characters()
    if not user_id:
        # Redireciona para o login se o usuário não estiver logado
        page.go("/")
        return

    create_character_button = ft.ElevatedButton(
        bgcolor="#000000",
        color="#FFFFFF",
        width=210,
        height=20,
        text="Criar Novo Personagem",
        on_click=lambda e: page.go("/create_character"),
    )

    # Função para deletar um personagem
    def handle_delete_character(e, char_id):
        delete_character(char_id)
        page.update()

    # Função para editar um personagem
    def handle_edit_character(e, char_id):
        prepare_character_for_edit(char_id, page)
        page.go("/edit_character")

    # Layout principal para exibir os personagens
    if not characters:
        content = ft.Column(
            controls=[
                ft.Text(
                    value="Nenhum personagem criado ainda.",
                    size=20,
                    weight="bold",
                    color="#ffffff",
                ),
                create_character_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        # Exibição de personagens criados
        character_cards = []
        for char in characters:
            character_cards.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"Nome: {char.name}", size=18, color="#ffffff"
                            ),
                            ft.Text(
                                f"Raça: {char.race}", size=16, color="#bbbbbb"
                            ),
                            ft.Text(
                                f"Classe: {char.clas}",
                                size=16,
                                color="#bbbbbb"
                            ),
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        on_click=lambda e,
                                        char_id=char.id:
                                        handle_edit_character(
                                            e, char_id
                                        ),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        on_click=lambda e,
                                        char_id=char.id:
                                        handle_delete_character(
                                            e, char_id
                                        ),
                                    ),
                                ]
                            ),
                        ]
                    ),
                    padding=10,
                    border=ft.border.all(1, color="#cccccc"),
                    bgcolor="#333333",
                    border_radius=10,
                )
            )

        # Define o conteúdo com personagens
        content = ft.Column(
            controls=[
                ft.Text(
                    value="Seus Personagens:",
                    size=25,
                    weight="bold",
                    color="#ffffff",
                ),
                *character_cards,
                create_character_button,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # Página principal
    character_page = ft.View(
        "/characters",
        [
            ft.Row(
                controls=[
                    ft.Container(
                        bgcolor="#212121",
                        width=850,
                        height=600,
                        border_radius=35,
                        padding=20,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    value="Personagens",
                                    size=45,
                                    color="#ffffff"
                                ),
                                content,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        ],
    )

    return character_page
