from models import Base
from util.db import get_db_engine
from settings import get_or_create_project_settings

settings = get_or_create_project_settings()
settings_db = settings.get_settings('db')
engine = get_db_engine(settings_db)
Base.metadata.create_all(engine)
