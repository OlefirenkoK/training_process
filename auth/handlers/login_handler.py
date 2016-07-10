from handlers.base_handler import BaseHandler


class LoginHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render('templates/login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        print(dir(self))
        self.redirect('/test/')
