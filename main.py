import flet as ft
from views.login import login_view
from views.register import register_view


def main(page: ft.Page):
    page.title = "Sistema de Login Modularizado"

    def route_change(route):
        page.views.clear()
        if page.route == "/login":
            page.views.append(login_view(page))
        elif page.route == "/register":
            page.views.append(register_view(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


ft.app(main)
