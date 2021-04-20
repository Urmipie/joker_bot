import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Like(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'likes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    joke_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('jokes.id'))
    user = orm.relation('User')
    joke = orm.relation('Joke')
