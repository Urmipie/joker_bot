import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Joke(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jokes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String)
