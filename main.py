import flet as ft
from models.database import init_db
from views.register import register_view
from views.login import login_view
from views.character import character_view
from views.create_character import create_character_view
import urllib.parse


def parse_route_params(route):
    if "?" in route:
        path, query = route.split("?", 1)
        params = urllib.parse.parse_qs(query)
        return path, {k: v[0] for k, v in params.items()}
    return route, {}


def main(page: ft.Page):
    page.title = "Infinity RPG"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.maximized = True
    page.window.minimized = False

    # Função para lidar com as mudanças de rotas/views
    def route_change(route):
        page.views.clear()
        path, params = parse_route_params(page.route)

        if path == "/":
            page.views.append(login_view(page))
        elif path == "/register":
            page.views.append(register_view(page))
        elif path == "/characters":
            page.views.append(character_view(page))
        elif path == "/create_character":
            # Passe os parâmetros (como character_id) para a view
            page.views.append(create_character_view(
                page, params.get("character_id")))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    init_db()
    ft.app(target=main, assets_dir='assets')
