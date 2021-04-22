import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

from datetime import datetime


class Subscribe(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'subscribes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user = orm.relation('User')
    subscriber = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    phrase = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    next_send = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())
    frequency = sqlalchemy.Column(sqlalchemy.Interval)
