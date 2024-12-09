import flet as ft


def login_view(page: ft.Page):
    return ft.View(
        "/login",
        controls=[
            ft.TextField(
                label="Username",
                autofocus=True,
            ),
            ft.TextField(
                label="Password",
                password=True,
                can_reveal_password=True,
            ),
            ft.ElevatedButton(
                "Login",
                on_click=lambda _: print("Login clicado!"),
            ),
            ft.ElevatedButton(
                "Cadastrar",
                on_click=lambda _: page.go("/register"),
            ),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
