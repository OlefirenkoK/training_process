import json
import tornado.web

from util.user_auth import get_user_object

# import logging
# logger = logging.getLogger('training_process.' + __name__)


class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    web_session_id_name = 'sess_id'

    def initialize(self):
        self.db = self.application.db

    def get_current_user(self):
        """Override to determine the current user from, e.g., a cookie. As user
        cookie is not set return None.

        This method may not be a coroutine.
        """
        username = self.get_secure_cookie(self.web_session_id_name, None)
        if username is not None:
            return username.decode('utf-8')
        else:
            return None

    def get_current_user_as_object(self):
        """Return current user as User instance."""
        username = self.get_current_user()
        if username is not None:
            return get_user_object(self, username)
        else:
            return None

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.
        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            # logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                # logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            # logger.debug("Returning default argument %s, as we couldn't find "
            #         "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        # logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg
