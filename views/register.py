import flet as ft
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

    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True)
    register_button = ft.ElevatedButton("Register", on_click=register_user)

    return ft.View(
        "/register",
        controls=[
            ft.Text("Register", size=30, weight="bold"),
            username_field,
            password_field,
            register_button,
        ],
    )
