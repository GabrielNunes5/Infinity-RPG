import flet as ft
from config import input_configs, btn_configs
from controllers.register_controller import UserController


def register_view(page: ft.Page):
    def handle_register(e):
        name = name_field.value
        username = username_field.value
        email = email_field.value
        password = password_field.value
        confirm_password = confirm_password_field.value

        # Validações
        errors = UserController.validade_user_data(
            name,
            username,
            email,
            password
        )

        if password != confirm_password:
            errors.append("As senhas não coincidem.")

        if errors:
            for error in errors:
                snack_bar = ft.SnackBar(ft.Text(error))
                page.snack_bar = snack_bar
                snack_bar.open = True
                page.update()
            return

        # Cadastro
        error_message = UserController.register_user(
            name,
            username,
            email,
            password
        )
        if error_message:
            snack_bar = ft.SnackBar(ft.Text(f'Erro: {error_message}'))
            page.snack_bar = snack_bar
            snack_bar.open = True
            page.update()
        else:
            snack_bar = ft.SnackBar(ft.Text("Usuário cadastrado com sucesso!"))
            page.snack_bar = snack_bar
            snack_bar.open = True
            page.update()
            page.go("/")

    def validate_password(e):
        """Validação em tempo real para a senha"""
        password = password_field.value
        if len(password) < 8:
            password_feedback.value = (
                "A senha deve ter pelo menos 8 caracteres.")
            password_feedback.color = "red"
        elif not any(c.isupper() for c in password):
            password_feedback.value = (
                "A senha deve conter pelo menos 1 letra maiúscula.")
            password_feedback.color = "red"
        elif not any(c.isdigit() for c in password):
            password_feedback.value = (
                "A senha deve conter pelo menos 1 número.")
            password_feedback.color = "red"
        elif not any(c in "!@#$%^&*()_+-=[]{}|;':,.<>?/" for c in password):
            password_feedback.value = (
                "A senha deve conter pelo menos 1 caractere especial.")
            password_feedback.color = "red"
        else:
            password_feedback.value = "Senha forte!"
            password_feedback.color = "green"
        page.update()

    def show_instructions(e):
        instructions_dialog.open = True
        page.update()

    # Campos do formulário
    name_field = ft.TextField(
        **input_configs,
        label="Nome e Sobrenome",
        icon=ft.Icons.DRIVE_FILE_RENAME_OUTLINE_ROUNDED)
    username_field = ft.TextField(
        **input_configs,
        label="Usuário",
        icon=ft.Icons.PERSON_ROUNDED)
    email_field = ft.TextField(
        **input_configs,
        label="Email",
        icon=ft.Icons.ALTERNATE_EMAIL_OUTLINED,
        suffix_text=".com",
    )
    password_field = ft.TextField(
        **input_configs,
        label="Senha",
        icon=ft.Icons.PASSWORD_OUTLINED,
        can_reveal_password=True,
        password=True,
        on_change=validate_password
    )
    confirm_password_field = ft.TextField(
        **input_configs,
        label="Confirme sua senha",
        icon=ft.Icons.PASSWORD_OUTLINED,
        can_reveal_password=True,
        password=True
    )
    password_feedback = ft.Text(value="", color="red")

    register_button = ft.ElevatedButton(
        "Cadastrar",
        **btn_configs,
        on_click=handle_register)
    login_redirect_text = ft.TextButton(
        "Já possui conta? Entre agora",
        on_click=lambda _: page.go("/"))

    # Botão de instruções
    instructions_button = ft.IconButton(
        icon=ft.Icons.INFO_OUTLINED,
        tooltip="Instruções de preenchimento",
        on_click=show_instructions
    )

    # Janela modal com instruções
    instructions_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Instruções de preenchimento"),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Nome e Sobrenome: Deve conter nome completo."),
                    ft.Text("Usuário: Escolha um nome único."),
                    ft.Text(
                        "Email: Deve ser valido: exemplo@dominio.com"),
                    ft.Text(
                        "Senha: Deve conter ao menos 8 caracteres, incluindo "
                        "1 letra maiúscula, 1 caractere especial e 1 número."
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=10,
            ),
            width=400,
            height=200,
            padding=10,
        ),
        actions=[
            ft.TextButton(
                "Fechar",
                on_click=lambda _: page.close(instructions_dialog),
            ),
        ],
    )

    # Estrutura da página
    register_page = ft.View(
        "/register",
        [
            ft.Row(
                controls=[
                    ft.Container(
                        bgcolor="#212121",
                        width=450,
                        height=550,
                        border_radius=35,
                        padding=20,
                        content=ft.Column(
                            controls=[
                                ft.Text(value='INFINITY RPG - CADASTRO',
                                        size=30,
                                        weight="bold",
                                        color="#ffffff",
                                        ),
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            value='Cadastre-se e jogue agora',
                                            size=20,
                                            color='#ffffff'),
                                        instructions_button],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),

                                name_field,
                                username_field,
                                email_field,
                                password_field,
                                confirm_password_field,
                                password_feedback,
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
                expand=True),
            instructions_dialog
        ])

    return register_page
