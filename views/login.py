import flet as ft
from config import input_configs, btn_configs
from controllers.login_controller import LoginController
from controllers.register_controller import UserController

# Armazena o ID do usuário logado
user_session = {"user_id": None}


def login_view(page: ft.Page):
    def clear_fields(*fields):
        """Função auxiliar para limpar campos."""
        for field in fields:
            field.value = ""

    def authenticate_user(e):
        username = username_field.value
        password = password_field.value

        result = LoginController.authenticate_user(username, password)

        if result["status"]:
            user_session["user_id"] = result["user_id"]
            page.go("/characters")
        else:
            snack_bar = ft.SnackBar(ft.Text(result["message"]))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    def verify_user_and_email(e):
        username = username_field_forgot.value
        email = email_field_forgot.value

        result = LoginController.verify_user_and_email(username, email)

        if result["status"]:
            forgot_psw_model.open = False
            reset_psw_model.open = True
        else:
            alert = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text("Usuário ou e-mail não cadastrado."),
                actions=[
                    ft.TextButton(
                        "Fechar", on_click=lambda _: page.close(alert))
                ],
            )
            page.dialog = alert
            alert.open = True

        clear_fields(username_field_forgot, email_field_forgot)
        page.update()

    def reset_password(e):
        username = username_field_forgot.value
        new_password = new_password_field.value
        confirm_password = confirm_password_field.value

        if new_password != confirm_password:
            alert = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text("As senhas não coincidem. Tente novamente."),
                actions=[
                    ft.TextButton(
                        "Fechar", on_click=lambda _: page.close(alert))
                ],
            )
            page.dialog = alert
            alert.open = True
        else:
            errors = UserController.validate_password(password=new_password)
            password_errors = [error for error in errors if "Senha" in error]

            if password_errors:
                alert = ft.AlertDialog(
                    title=ft.Text("Erro"),
                    content=ft.Text("\n".join(password_errors)),
                    actions=[
                        ft.TextButton(
                            "Fechar", on_click=lambda _: page.close(alert))
                    ],
                )
                page.dialog = alert
                alert.open = True
            else:
                result = LoginController.update_password(
                    username, new_password)

                if result["status"]:
                    snack_bar = ft.SnackBar(
                        ft.Text("Senha redefinida com sucesso!"))
                    page.overlay.append(snack_bar)
                    snack_bar.open = True
                    reset_psw_model.open = False
                else:
                    alert = ft.AlertDialog(
                        title=ft.Text("Erro"),
                        content=ft.Text(
                            "Erro ao atualizar a senha. Tente novamente."),
                        actions=[
                            ft.TextButton(
                                "Fechar", on_click=lambda _: page.close(alert))
                        ],
                    )
                    page.dialog = alert
                    alert.open = True

        clear_fields(new_password_field, confirm_password_field)
        page.update()

    def show_forgot_psw_modal(e):
        forgot_psw_model.open = True
        page.update()

    # Campos da interface
    username_field = ft.TextField(
        **input_configs, label="Usuário", icon=ft.Icons.PERSON_ROUNDED
    )
    password_field = ft.TextField(
        **input_configs,
        label="Senha",
        password=True,
        icon=ft.Icons.LOCK_OUTLINE,
        can_reveal_password=True,
    )
    login_button = ft.ElevatedButton(
        **btn_configs, text="Entrar", on_click=authenticate_user
    )
    register_redirect_text = ft.TextButton(
        "Não possui conta? Cadastre-se agora",
        on_click=lambda _: page.go("/register")
    )
    forgot_password_text = ft.TextButton(
        "Esqueci a conta", on_click=show_forgot_psw_modal
    )

    # Modal de "Esqueci a senha"
    username_field_forgot = ft.TextField(
        **input_configs, label="Usuário", icon=ft.Icons.PERSON_OUTLINE
    )
    email_field_forgot = ft.TextField(
        **input_configs, label="E-mail", icon=ft.Icons.ALTERNATE_EMAIL
    )
    forgot_psw_model = ft.AlertDialog(
        modal=True,
        title=ft.Text("Recuperar Senha"),
        content=ft.Container(
            content=ft.Column(
                controls=[username_field_forgot, email_field_forgot],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=300,
            height=100,
            padding=5,
        ),
        actions=[
            ft.TextButton(
                "Fechar",
                on_click=lambda _: (
                    page.close(forgot_psw_model),
                    clear_fields(username_field_forgot, email_field_forgot),
                    page.update(),
                ),
            ),
            ft.TextButton("Verificar", on_click=verify_user_and_email),
        ],
    )

    # Modal para redefinir senha
    new_password_field = ft.TextField(
        **input_configs,
        label="Nova Senha",
        password=True,
        can_reveal_password=True,
        icon=ft.Icons.LOCK_OUTLINE,
    )
    confirm_password_field = ft.TextField(
        **input_configs,
        label="Confirmar Nova Senha",
        password=True,
        can_reveal_password=True,
        icon=ft.Icons.LOCK_OUTLINE,
    )
    reset_psw_model = ft.AlertDialog(
        modal=True,
        title=ft.Text("Redefinir Senha"),
        content=ft.Container(
            content=ft.Column(
                controls=[new_password_field, confirm_password_field],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=300,
            height=100,
            padding=5,
        ),
        actions=[
            ft.TextButton(
                "Fechar",
                on_click=lambda _: (
                    page.close(reset_psw_model),
                    clear_fields(new_password_field, confirm_password_field),
                    page.update(),
                ),
            ),
            ft.TextButton("Redefinir", on_click=reset_password),
        ],
    )

    # Estrutura da página
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
                                ft.Text(
                                    value="INFINITY RPG - LOGIN",
                                    size=30,
                                    weight="bold",
                                    color="#ffffff"),
                                ft.Image(src="images/d20.png",
                                         width=80,
                                         color="#ffffff"),
                                ft.Text(value="Entre e divirta-se",
                                        size=20,
                                        color="#ffffff"),
                                username_field,
                                password_field,
                                login_button,
                                register_redirect_text,
                                forgot_password_text,
                                forgot_psw_model,
                                reset_psw_model,
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
