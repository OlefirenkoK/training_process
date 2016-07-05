import json

from models import User
from util.db import get_db_session
from settings import get_or_create_project_settings
from util.user_auth import hash_password


settings_db = None
connection_db = None


def _get_settings_db():
    if settings_db is None:
        settings = get_or_create_project_settings()
        return settings.get_settings('db')
    return settings_db


def _get_connection_db():
    global connection_db
    if connection_db is None:
        settings = _get_settings_db()
        Session = get_db_session(settings)
        connection_db = Session()
    return connection_db


def _user_need_to_change(data, name):
    _data = data.get(name, None)
    for row in _data:
        row['password'] = hash_password(row['password'])


class Provision:

    data_map = None
    file = 'provision_data.json'

    @classmethod
    def _init_data(cls, fp, *args, **kwargs):
        if cls.data_map is None:
            cls.data_map = cls._get_provision_data()
        if fp:
            fp(cls.data_map, *args, **kwargs)

    @classmethod
    def _get_rows(cls, name):
        print(name)
        print(cls.data_map)
        for row in cls.data_map.get(name):
            yield row

    @classmethod
    def _get_provision_data(cls):
        fp = open(cls.file)
        return json.loads(fp.read())

    def __init__(self, obj_name, name, need_to_change=None):
        self.obj_name = obj_name
        self.name = name
        self._init_data(need_to_change, name=name)
        self._provision()

    def _provision(self):
        connection = _get_connection_db()
        insert_data = self._get_rows(self.name)
        for data in insert_data:
            obj = self.obj_name(**data)
            # connection.execute(self.obj_name.insert(), list(insert_data))
            connection.add(obj)
        connection.commit()

if __name__ == '__main__':
    user = Provision(User, 'user', _user_need_to_change)
