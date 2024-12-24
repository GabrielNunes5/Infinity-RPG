from bcrypt import hashpw, gensalt, checkpw

# Definições gerais
input_configs = {
    'border': "underline",
    'width': 300,
    'text_size': 15,
}
atribute_configs = {
    'width': 100,
    'value': "8"
}
btn_configs = {
    'bgcolor': '#000000',
    'color': '#FFFFFF',
    'width': 130,
    'height': 35
}

DND_RACES = [
    "Humano",
    "Elfo",
    "Anão",
    "Meio-Orc",
    "Halfling",
    "Tiefling",
    "Gnomo",
    "Dragonborn"
]

HAIR_COLORS = [
    {"name": "Preto", "hex": "#000000"},
    {"name": "Castanho", "hex": "#8B4513"},
    {"name": "Loiro", "hex": "#FFD700"},
    {"name": "Ruivo", "hex": "#FF4500"},
    {"name": "Branco", "hex": "#FFFFFF"},
]
SKIN_COLORS = [
    {"name": "Preto", "hex": "#3B2F2F"},
    {"name": "Marrom Escuro", "hex": "#4E3629"},
    {"name": "Marrom Médio", "hex": "#8B5A2B"},
    {"name": "Marrom Claro", "hex": "#C69C6D"},
    {"name": "Pálido", "hex": "#F5CBA7"},
    {"name": "Muito Claro", "hex": "#FFDBAC"}
]


def hash_password(password: str) -> str:
    """Criptografa uma senha usando bcrypt."""
    return hashpw(password.encode(), gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta."""
    return checkpw(plain_password.encode(), hashed_password.encode())
