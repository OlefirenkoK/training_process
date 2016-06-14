import tornado.httpserver
import tornado.ioloop
import tornado.web

from settings import get_project_settings
from base_urls import url_patterns


class TrainingProcessApplication(tornado.web.Application):

    def __getattr__(self, item):
        if item in self.__dict__:
            return self[item]
        raise AttributeError

    def __init__(self):
        self._settings = get_project_settings()
        tornado.web.Application.__init__(self, url_patterns, **self._settings)


def main():
    app = TrainingProcessApplication()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(app._settings.run.port)
    print(app._settings.run.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
