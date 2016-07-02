from handlers.test_handler import TestHandler
from auth.auth_urls import url_pattern as auth_url_pattern


url_patterns = [
    (r'/test/?', TestHandler),
]

url_patterns.extend(auth_url_pattern)
