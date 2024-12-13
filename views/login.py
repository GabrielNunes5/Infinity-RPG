import flet as ft
from config import input_configs, btn_configs
from controllers.login_controller import LoginController

# Armazena o ID do usuário logado
user_session = {"user_id": None}


def login_view(page: ft.Page):
    def authenticate_user(e):
        username = username_field.value
        password = password_field.value

        # Use o controller para autenticação
        result = LoginController.authenticate_user(username, password)

        if result["status"]:
            user_session["user_id"] = result["user_id"]
            # print(f"Usuário {result['username']} logado com sucesso!")
            page.go("/characters")
        else:
            snack_bar = ft.SnackBar(ft.Text(result["message"]))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    # Campos da interface
    username_field = ft.TextField(
        **input_configs,
        label="Usuário",
        icon=ft.Icons.PERSON_ROUNDED)
    password_field = ft.TextField(
        **input_configs,
        label="Senha",
        password=True,
        icon=ft.Icons.PASSWORD_OUTLINED,
        can_reveal_password=True)
    login_button = ft.ElevatedButton(
        **btn_configs,
        text="Entrar",
        on_click=authenticate_user)
    register_redirect_text = ft.TextButton(
        "Não possui conta? Cadastre-se agora",
        on_click=lambda _: page.go("/register"))

    # Página de login
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
