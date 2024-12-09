import flet as ft
from models.database import SessionLocal
from models.user import User
from config import verify_password


def login_view(page: ft.Page):
    def login_user(e):
        session = SessionLocal()
        username = username_field.value
        password = password_field.value
        user = session.query(User).filter(User.username == username).first()
        if user and verify_password(password, user.password):
            page.go("/character")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid credentials!"))
            page.snack_bar.open()
        session.close()

    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True)
    login_button = ft.ElevatedButton("Login", on_click=login_user)

    return ft.View(
        "/login",
        controls=[
            ft.Text("Login", size=30, weight="bold"),
            username_field,
            password_field,
            login_button,
        ],
    )
