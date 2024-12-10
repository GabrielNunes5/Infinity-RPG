import flet as ft
from models.database import SessionLocal
from models.user import User
from bcrypt import checkpw

user_session = {"user_id": None}  # Armazena o ID do usuário logado


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

    username_field = ft.TextField(label="Username", width=300)
    password_field = ft.TextField(
        label="Password", password=True, can_reveal_password=True, width=300)
    login_button = ft.ElevatedButton(text="Login", on_click=authenticate_user)
    register_button = ft.ElevatedButton(
        text="Cadastrar", on_click=lambda _: page.go("/register")
    )

    return ft.View(
        "/",
        [
            ft.Column(
                controls=[
                    username_field,
                    password_field,
                    login_button,
                    register_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
    )
