import flet as ft
from config import input_configs, btn_configs
from models.database import SessionLocal
from models.user import User
from config import hash_password


def register_view(page: ft.Page):
    def register_user(e):
        session = SessionLocal()
        username = username_field.value
        password = hash_password(password_field.value)
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        session.close()
        page.go("/")

    username_field = ft.TextField(
        **input_configs,
        label="Usuário")
    email_field = ft.TextField(
        **input_configs,
        label="Email",
        suffix_text=".com",
    )
    password_field = ft.TextField(
        **input_configs,
        label="Senha",
        password=True)
    register_button = ft.ElevatedButton(
        "Cadastrar",
        **btn_configs,
        on_click=register_user)
    login_redirect_text = ft.TextButton(
        "Já possui conta? Entre agora",
        on_click=lambda _: page.go("/"))
    register_page = ft.View(
        "/register",
        [
            ft.Row(
                controls=[
                    ft.Container(
                        bgcolor="#212121",
                        width=450,
                        height=500,
                        border_radius=35,
                        padding=20,
                        content=ft.Column(
                            controls=[
                                ft.Text(value='INFINITY RPG - CADASTRO',
                                        size=30,
                                        weight="bold",
                                        color="#ffffff",
                                        ),
                                ft.Text(value='Cadastre-se e jogue agora',
                                        size=20,
                                        color='#ffffff',
                                        ),
                                username_field,
                                email_field,
                                password_field,
                                register_button,
                                login_redirect_text
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,)],)

    return register_page
