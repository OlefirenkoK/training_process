from tornado.web import StaticFileHandler

from handlers.test_handler import TestHandler
from auth.auth_urls import url_pattern as auth_url_pattern
from settings import get_project_settings_config_item


url_patterns = [
    (
        r'/static/(.*)',
        StaticFileHandler,
        get_project_settings_config_item('dev', 'static_path')
    ),
    (r'/test/?', TestHandler),
]

url_patterns.extend(auth_url_pattern)
