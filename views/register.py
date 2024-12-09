import flet as ft


def register_view(page: ft.Page):
    return ft.View(
        "/register",
        controls=[
            ft.Text("Registro de Usuário"),
            ft.TextField(label="Username"),
            ft.TextField(label="Password", password=True),
            ft.TextField(label="Confirm Password", password=True),
            ft.ElevatedButton(
                "Registrar",
                on_click=lambda _: page.go("/login"),
            ),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
