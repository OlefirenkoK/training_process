from handlers.base_handler import BaseHandler

import logging
logger = logging.getLogger('training_process.' + __name__)


class TestHandler(BaseHandler):
    def get(self):
        self.write('Application works!')
