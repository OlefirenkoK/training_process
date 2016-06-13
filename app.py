import tornado.httpserver
import tornado.ioloop
import tornado.web

from settings import MainSetting
from base_urls import url_patterns


class TornadoTrainingProcess(tornado.web.Application):
    def __init__(self):
        self._settings = MainSetting()
        tornado.web.Application.__init__(self, url_patterns, **self._settings)


def main():
    app = TornadoTrainingProcess()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(app.settings['port'])
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
