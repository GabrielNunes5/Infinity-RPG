import flet as ft
from models.database import SessionLocal
from models.character import Character


def character_view(page: ft.Page):
    def save_character(e):
        session = SessionLocal()
        char = Character(
            user_id=1,  # Substitua pelo ID do usuário logado
            name=name_field.value,
            strength=int(strength_slider.value),
            intelligence=int(intelligence_slider.value),
            skin_color=skin_color_field.value,
            hair=hair_field.value,
        )
        session.add(char)
        session.commit()
        session.close()
        page.snack_bar = ft.SnackBar(ft.Text("Character saved!"))
        page.snack_bar.open()

    name_field = ft.TextField(label="Name")
    strength_slider = ft.Slider(min=1, max=10, divisions=9, label="Strength")
    intelligence_slider = ft.Slider(
        min=1, max=10, divisions=9, label="Intelligence")
    skin_color_field = ft.TextField(label="Skin Color")
    hair_field = ft.TextField(label="Hair")

    save_button = ft.ElevatedButton("Save", on_click=save_character)

    return ft.View(
        "/character",
        controls=[
            ft.Text("Character Customization", size=30, weight="bold"),
            name_field,
            strength_slider,
            intelligence_slider,
            skin_color_field,
            hair_field,
            save_button,
        ],
    )
