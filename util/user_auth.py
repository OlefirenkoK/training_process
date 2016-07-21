import hashlib
import hmac

from sqlalchemy import or_

from settings import get_project_settings_config_item
from models import User


salt = get_project_settings_config_item('db', 'salt')
salt = salt.encode('utf-8')


def hash_password(password):
    if not isinstance(password, bytes):
        password = password.encode('utf-8')
    hash_pwd = hmac.new(
        digestmod=hashlib.sha256,
        key=salt,
        msg=password.strip()
    )
    return hash_pwd.hexdigest()


def get_user_with_email(handler, email_or_name):
    """Function for detect user by email or username.
        - `handler` - Handler object.
        - `email_or_name` - parameter for detect user.
    """
    return handler.db.query(User).filter(or_(
        User.email == email_or_name, User.name == email_or_name)).first()


def get_user_object(handler, name):
    """Return user object (instance of User class). If user is not defined
    return None.
        - `handler` - Handler object.
        - `name` - user name as string.
    """
    return handler.db.query(User).filter(User.name == name).first()


def is_success_authorization(handler, user, password):
    """Function for authorization users. If password is valid the secret will
    be cookie and return True else return False.
        - `handler` - Handler object.
        - `user` - user object, must be User instance.
        - `password` - user password for verification.
    """
    if user.password == hash_password(password):
        handler.set_secure_cookie(handler.web_session_id_name, user.name)
        return True
    else:
        return False
