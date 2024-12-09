import flet as ft
from models.database import init_db
from views.home import home_view
from views.register import register_view
from views.login import login_view
from views.character import character_view


def main(page: ft.Page):
    page.title = "Character Creator"

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(home_view(page))
        elif page.route == "/register":
            page.views.append(register_view(page))
        elif page.route == "/login":
            page.views.append(login_view(page))
        elif page.route == "/character":
            page.views.append(character_view(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    init_db()
    ft.app(target=main)
