import flet as ft
from controllers.character_controller import (
    load_characters, delete_character, prepare_character_for_edit
)


def character_view(page: ft.Page):
    # Carrega os personagens do usuário logado
    user_id, characters = load_characters()
    if not user_id:
        # Redireciona para o login se o usuário não estiver logado
        page.go("/")
        return

    # Botão para criar um novo personagem
    create_character_button = ft.ElevatedButton(
        bgcolor="#000000",
        color="#FFFFFF",
        width=210,
        height=25,
        text="Criar Novo Personagem",
        on_click=lambda e: page.go("/create_character"),
    )

    # Criação de uma ListView para exibir os personagens
    content = ft.ListView(
        spacing=10,
        padding=10,
        auto_scroll=False,
        expand=True,
    )

    # Texto para fazer logout
    logout = ft.TextButton(
        "Sair da conta",
        on_click=lambda e: handle_logout(e, page)
    )

    def handle_logout(e, page):
        # Lógica para fazer logout do sistema
        page.session.clear()
        page.go("/")

    # Função para atualizar a lista de personagens
    def update_character_list():
        # Limpa os controles existentes
        content.controls.clear()
        # Mensagem caso não haja nenhum personagem criado
        if not characters:
            content.controls.append(
                ft.Container(
                    content=ft.Text(
                        value="Nenhum personagem criado ainda.",
                        size=20,
                        weight="bold",
                        color="#ffffff",
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )
        else:
            # Caso haja personagens, cria um card para cada um
            for char in characters:
                card = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"Nome: {char.name}",
                                    size=18, color="#ffffff"),
                            ft.Image(src=char.class_image,
                                     width=100, height=100),
                            ft.Text(f"Raça: {char.race}",
                                    size=16, color="#bbbbbb"),
                            ft.Text(f"Classe: {char.clas}",
                                    size=16, color="#bbbbbb"),
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.SPORTS_MMA_SHARP,
                                            color="#FF8C00"),
                                    ft.Text(
                                        f"Força: {char.strength}",
                                        size=16, color="#bbbbbb"),
                                    ft.Icon(ft.Icons.FAVORITE,
                                            color="#FF0000"),
                                    ft.Text(
                                        f"Constituição: {char.constitution}",
                                        size=16, color="#bbbbbb"),
                                    ft.Icon(ft.Icons.DIRECTIONS_RUN,
                                            color="#FFFF00"),
                                    ft.Text(
                                        f"Destreza:{char.dexterity}",
                                        size=16, color="#bbbbbb"),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.MENU_BOOK_SHARP,
                                            color="#00FFFF"),
                                    ft.Text(
                                        f"Inteligência:{char.intelligence}",
                                        size=16, color="#bbbbbb"),
                                    ft.Icon(ft.Icons.SCHOOL_SHARP,
                                            color="#8A2BE2"),
                                    ft.Text(
                                        f"Sabedoria: {char.wisdom}",
                                        size=16, color="#bbbbbb"),
                                    ft.Icon(ft.Icons.EMOJI_PEOPLE,
                                            color="#FF69B4"),
                                    ft.Text(
                                        f"Carisma: {char.charisma}",
                                        size=16, color="#bbbbbb"),
                                ]),
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_color="#2149ad",
                                        on_click=lambda e, char_id=char.id:
                                        handle_edit_character(
                                            e, char_id),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color="#ad2121",
                                        on_click=lambda e, char_id=char.id:
                                        handle_delete_character(
                                            e, char_id),
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
                content.controls.append(card)

    def handle_delete_character(e, char_id):
        # Exclui o personagem e atualiza a lista
        delete_character(char_id)
        # Remove o personagem da lista local e atualiza a exibição
        nonlocal characters
        characters = [char for char in characters if char.id != char_id]
        update_character_list()
        page.update()

    def handle_edit_character(e, char_id):
        # Prepara a edição do personagem e redireciona para a tela de edição
        prepare_character_for_edit(char_id, page)
        print(f"Editando personagem {char_id}")
        page.go(f"/create_character?character_id={char_id}")

    # Atualiza a lista de personagens inicialmente
    update_character_list()

    # Estrutura da página
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
                                    value="Seus Personagens:",
                                    size=25,
                                    weight="bold",
                                    color="#ffffff",
                                ),
                                content,
                                create_character_button,
                                logout
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
