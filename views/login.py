import flet as ft
from config import input_configs, btn_configs
from models.database import SessionLocal
from models.user import User
from bcrypt import checkpw

# Armazena o ID do usuário logado
user_session = {"user_id": None}


def login_view(page: ft.Page):
    def authenticate_user(e):
        session = SessionLocal()
        username = username_field.value
        password = password_field.value
        user = session.query(User).filter_by(username=username).first()
        session.close()

        if user and checkpw(password.encode(), user.password.encode()):
            user_session["user_id"] = user.id
            print(f"Usuário {user.username} logado com sucesso!")
            page.go("/characters")
        else:
            snack_bar = ft.SnackBar(ft.Text("Credenciais inválidas!"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    username_field = ft.TextField(
        **input_configs,
        label="Usuário",
        icon=ft.Icons.PERSON_ROUNDED)
    password_field = ft.TextField(
        **input_configs,
        label="Senha",
        password=True,
        icon=ft.Icons.KEY,
        can_reveal_password=True)
    login_button = ft.ElevatedButton(
        **btn_configs,
        text="Entrar",
        on_click=authenticate_user)
    register_redirect_text = ft.TextButton(
        "Não possui conta? Cadastre-se agora",
        on_click=lambda _: page.go("/register"))

    login_page = ft.View(
        "/",
        [
            ft.Row(
                controls=[
                    ft.Container(
                        bgcolor="#212121",
                        width=400,
                        height=450,
                        border_radius=35,
                        padding=20,
                        content=ft.Column(
                            controls=[
                                ft.Text(value='INFINITY RPG - LOGIN',
                                        size=30,
                                        weight="bold",
                                        color="#ffffff",
                                        ),
                                ft.Image(
                                    src='assets/d20.png',
                                    width=80,
                                    color='#ffffff'
                                ),
                                ft.Text(value='Entre e divirta-se',
                                        size=20,
                                        color='#ffffff',
                                        ),
                                username_field,
                                password_field,
                                login_button,
                                register_redirect_text
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        ],
    )

    return login_page
