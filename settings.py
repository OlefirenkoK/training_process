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
            login=self.settings['psql_login'],
            password=self.settings['psql_password'],
            host=self.settings['psql_host'],
            port=self.settings['psql_port'],
            dbname=self.settings['psql_dbname']
        )


class RunSetting(FabricSettings):

    """Base class for project settings. Used default_settings if there are no
    others."""

    default_settings = DefaultRunSettings()
    _id = 'run'


class SettingCollector(dict):

    collector = [
        RunSetting,
        DBSettings,
    ]

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


def get_project_settings():
    pass


if __name__ == '__main__':
    # settings = RunSetting()  # {'rrr': 1, 'port': 8000}
    # print(settings)
    # db_settings = DBSettings()   # {'psql_host': '8.8.8.8'}
    # print(db_settings)
    settings = SettingCollector()
    print(type(settings.run))
