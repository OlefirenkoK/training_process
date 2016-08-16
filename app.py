import tornado.httpserver
import tornado.ioloop
import tornado.web

from settings import get_or_create_project_settings
from base_urls import url_patterns
from util.db import get_db_session


class TrainingProcessApplication(tornado.web.Application):

    def __getattr__(self, item):
        if item in self.__dict__:
            return self[item]
        raise AttributeError

    def __init__(self):
        self._settings = get_or_create_project_settings()
        db_settings = self.config.get_settings('db')
        Session = get_db_session(db_settings)
        self.db = Session()
        tornado.web.Application.__init__(self, url_patterns, **self._settings)

    @property
    def config(self):
        return self._settings

    @config.setter
    def config(self, *args, **kwargs):
        raise NotImplemented

    @config.deleter
    def config(self):
        raise NotImplemented


def app_autoreload(app, timeout):
    """Set application autoreload. This option available only on Debug mod."""

    if app.config.get_settings_item('run', 'debug'):
        from tornado import autoreload
        autoreload.start(
            io_loop=tornado.ioloop.IOLoop.current(),
            check_time=2
        )


def info(config):
    print('Server is running host={0} port={1} debug={2}'.format(
        config.get_settings_item('run', 'host'),
        config.get_settings_item('run', 'port'),
        config.get_settings_item('run', 'debug'))
    )


def main():
    app = TrainingProcessApplication()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(app.config.get_settings_item('run', 'port'))
    app_autoreload(app, 2)
    main_loop = tornado.ioloop.IOLoop.instance()
    main_loop.spawn_callback(info, app.config)
    main_loop.start()


if __name__ == "__main__":
    main()
