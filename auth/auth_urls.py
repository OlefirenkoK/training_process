from auth.handlers.login_handler import LoginHandler


url_pattern = [
    (r'^auth/login/', LoginHandler),
]