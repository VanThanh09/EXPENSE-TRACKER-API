from datetime import datetime

from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    avatar = Column(String(150), default='https://res.cloudinary.com/drzc4fmxb/image/upload/v1733907010/xvethjfe9cycrroqi7po.jpg')


class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    author = relationship('User', backref='blogs', lazy=True)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class BlogImage(Base):
    __tablename__ = 'blogimage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text, nullable=False)

    blog_id = Column(Integer, ForeignKey('blog.id', ondelete='CASCADE'), nullable=False)
    blog = relationship('Blog', backref='images', lazy=True, passive_deletes=True)


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref='comments', lazy=True)

    blog_id = Column(Integer, ForeignKey('blog.id'))
    blog = relationship('Blog', backref='comments', lazy=True)


class Follow(Base):
    __tablename__ = 'follow'

    id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('user.id')) # người đi follow
    following_id = Column(Integer, ForeignKey('user.id')) # người được follow

    following = relationship('User', backref='following', lazy=True, foreign_keys=[follower_id]) # list user mình follow
    follower = relationship('User', backref='my_follower', lazy=True, foreign_keys=[following_id]) # list user follow mình


class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    blog_id = Column(Integer, ForeignKey('blog.id'), nullable=False)

    user = relationship('User', backref='likes', lazy=True)
    blog = relationship('Blog', backref='likes', lazy=True)


class Notification(Base):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String(32), nullable=False, default='BLOG')
    target_id = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='notifications', lazy=True)