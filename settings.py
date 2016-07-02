class FabricDefaultSettings(dict):

    def __init__(self):
        self.settings = None
        super().__init__(**self.default_settings)

    def _default_settings(self):
        """Base method for initialization default settings. This method must
        return dictionary with settings parameters."""
        return {}

    @property
    def default_settings(self):
        if self.settings is None:
            self.settings = self._default_settings()
        return self.settings

    def _update(self, default_settings, F):
        """Helper function for update method"""
        if default_settings is None:
            super().update()
            return
        for key in default_settings.copy():
            if key not in self.default_settings:
                default_settings.pop(key)
        super().update(**default_settings, **F)

    def update(self, default_settings=None, **F):
        """Overriding update method. Now it must return self
        (dictionary with settings)."""
        self._update(default_settings, F)
        return self


class FabricSettings(dict):

    _id = None
    default_settings = FabricDefaultSettings()

    @classmethod
    def get_id(self):
        return self._id

    def __getattr__(self, item):
        if item in self:
            return self[item]
        raise AttributeError

    def __init__(self, settings=None):
        self.settings = self.default_settings.update(settings)
        super().__init__(**self.settings)


class DefaultRunSettings(FabricDefaultSettings):

    """Default project settings. All settings must be writen in
    default_settings property method"""

    def _default_settings(self):
        settings = super()._default_settings()
        settings['host'] = '127.0.0.1'
        settings['port'] = 8888
        settings['debug'] = True
        return settings


class DefaultDBSettings(FabricDefaultSettings):

    def _default_settings(self):
        settings = {}
        settings['psql_login'] = 'flash'
        settings['psql_password'] = 'bkk.pbz'
        settings['psql_host'] = 'localhost'
        settings['psql_port'] = 11111
        settings['psql_dbname'] = 'tp'
        return settings


class DBSettings(FabricSettings):

    POSTGRES_PATTERN = 'postgresql://{login}:{password}@{host}:{port}/{dbname}'
    default_settings = DefaultDBSettings()
    _id = 'db'

    def __init__(self, settings=None):
        super().__init__(settings)
        self.db_url = self.get_db_url()

    def get_db_url(self):
        return self.POSTGRES_PATTERN.format(
            login=self['psql_login'],
            password=self['psql_password'],
            host=self['psql_host'],
            port=self['psql_port'],
            dbname=self['psql_dbname']
        )

    @property
    def debug(self):
        return get_debug_status()

    @debug.setter
    def debug(self):
        raise PermissionError

    @debug.deleter
    def debug(self):
        raise PermissionError


class RunSetting(FabricSettings):

    """Base class for project settings. Used default_settings if there are no
    others."""

    default_settings = DefaultRunSettings()
    _id = 'run'


class SettingCollector(dict):

    __init = None
    collector = [
        RunSetting,
        DBSettings,
    ]

    def __new__(cls, *args, **kwargs):
        if cls.__init is None:
            cls.__init = super().__new__(cls, *args, **kwargs)
        return cls.__init

    def __getattr__(self, item):
        if item in self:
            return self[item]
        raise AttributeError

    def __init__(self, **kwargs):
        settings = {}
        for config in self.collector:
            _id = config.get_id()
            item_settings = kwargs.get(_id, None)
            settings[_id] = config(item_settings)
        super().__init__(settings)

    def get_settings(self, _id):
        """Return setting by input name.
            - `_id` - name of settings.
        """
        return self[_id]

    def get_settings_item(self, _id, item):
        """Return config argument
            - `_id` - name of settings.
            - `item` - name of settings item.
        """

        settings = self.get_settings(_id)
        return settings[item]


def get_or_create_project_settings(**kwargs):
    """Abstract function for initialization settings. If project settings was
    created return it.
        `kwargs`: given settings, the key must be same as one of `_id`
                  of Setting classes.
        return: union project settings. Components settings separate by `_id`.
    """
    return SettingCollector(**kwargs)


def get_project_settings_config(name):
    """Return project settings config part by input name.
        - `name` - config name.
    """
    settings_controller = get_or_create_project_settings()
    return settings_controller.get_settings(name)


def get_debug_status():
    """Settings interface. Return debug status."""
    settings = get_or_create_project_settings()
    return settings.get_settings_item('run', 'debug')


if __name__ == '__main__':
    settings = get_or_create_project_settings(
        run={'rrr': 1, 'port': 8000},
        db={'psql_host': '8.8.8.8'}
    )
