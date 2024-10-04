from sqlalchemy import Column, Integer, String, Boolean

from src.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(255), unique=False, nullable=True)
    last_name = Column(String(255), unique=False, nullable=True)
    profession = Column(String(255), unique=False, nullable=True)
    lang = Column(String(5), unique=False, nullable=True, default="en")
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
