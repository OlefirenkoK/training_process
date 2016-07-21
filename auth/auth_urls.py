from auth.handlers.login_handler import LoginHandler, LogoutHandler


url_pattern = [
    (r'/auth/login/', LoginHandler),
    (r'/auth/logout/', LogoutHandler),
]
