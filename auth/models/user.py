from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from models import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String(80), nullable=False)
    date_join = Column(DateTime, default=datetime.now(), nullable=True)
    last_login = Column(DateTime, default=datetime.now(), nullable=True)
    password = Column(String(120), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
