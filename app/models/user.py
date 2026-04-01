from sqlalchemy import Integer, String, Column, DateTime, Boolean, ForeignKey
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    avatar = Column(String(150), default='https://res.cloudinary.com/drzc4fmxb/image/upload/v1733907010/xvethjfe9cycrroqi7po.jpg')