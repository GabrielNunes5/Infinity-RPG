import flet as ft
from models.database import SessionLocal
from models.character import Character
from views.login import user_session


def character_view(page: ft.Page):
    def create_character(e):
        if user_session["user_id"] is None:
            snack_bar = ft.SnackBar(ft.Text("Erro: usuário não autenticado!"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return

        session = SessionLocal()
        character_name = name_field.value
        strength = int(strength_field.value)
        intelligence = int(intelligence_field.value)
        user_id = user_session["user_id"]  # ID do usuário logado

        character = Character(name=character_name, strength=strength,
                              intelligence=intelligence, user_id=user_id)
        session.add(character)
        session.commit()
        session.close()

        snack_bar = ft.SnackBar(ft.Text(
            f"Personagem {character_name} criado com sucesso!"))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    name_field = ft.TextField(label="Nome do Personagem", width=300)
    strength_field = ft.TextField(label="Força (1-10)", width=300)
    intelligence_field = ft.TextField(label="Inteligência (1-10)", width=300)
    create_button = ft.ElevatedButton(
        text="Criar Personagem", on_click=create_character)

    return ft.View(
        "/characters",
        [
            ft.Column(
                controls=[
                    name_field,
                    strength_field,
                    intelligence_field,
                    create_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
    )
