from handlers.base_handler import BaseHandler
from util.user_auth import get_user_with_email, is_success_authorization


class LoginHandler(BaseHandler):

    def get(self, *args, **kwargs):
        user_cookie = self.get_secure_cookie(self.web_session_id_name, None)
        if user_cookie is not None:
            self.redirect('/test/')
        self.render('templates/login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        user = get_user_with_email(self, username)
        if user is None or password is None:
            self.render('templates/login.html')
        if is_success_authorization(self, user, password):
            self.redirect('/test/')
        else:
            self.redirect('/auth/login/')


class LogoutHandler(BaseHandler):

    def get(self, *args, **kwargs):
        """Logs out a user."""
        self.clear_all_cookies()
        self.redirect('/test/')
