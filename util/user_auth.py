import hashlib
import hmac

from settings import get_project_settings_config_item


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
