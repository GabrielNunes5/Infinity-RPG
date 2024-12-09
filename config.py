# input_configs = {
#     'border': "underline",
#     'width': 320,
#     'text_size': 14,
# }
# btn_configs = {
#     'bgcolor': '#000000',
#     'color': '#FFFFFF',
#     'width': 130,
#     'height': 20
# }

from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> str:
    """Criptografa uma senha usando bcrypt."""
    return hashpw(password.encode(), gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta."""
    return checkpw(plain_password.encode(), hashed_password.encode())
