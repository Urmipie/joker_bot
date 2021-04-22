from jokes.Joker import Joker
from sqlalchemy.exc import IntegrityError as SQLIntegrityError
from data.db_session import create_session
from data.users import User
from data.subscribes import Subscribe
from data.likes import Like

from datetime import timedelta


class Action:
    def __init__(self):
        self.joker = Joker()

    @staticmethod
    def new_user(vk_id=None, **kwargs):
        """
        :param kwargs: vk_id - айдишник вк
        :return:
        """
        sess = create_session()
        try:
            sess.add(User(vk_id=vk_id))
        except SQLIntegrityError:
            return 'Вы уже зарегестрированы'
        sess.commit()
        return 'Вы зарегистрированы!'

    def del_user(self, vk_id=None, **kwargs):
        """
        :param vk_id: айди вк
        :param kwargs: сборщик прочих аргументов
        :return:
        """
        assert vk_id
        sess = create_session()
        user = sess.query(User).filter(User.vk_id == vk_id).first()
        if user:
            for subscribe in sess.query(Subscribe).filter(Subscribe.subscriber == user.id):
                sess.delete(subscribe)
            for like in sess.query(Like).filter(Like.user_id == user.id):
                sess.delete(like)
            sess.delete(user)
            sess.commit()
            return 'Профиль успешно удалён'
        else:
            return 'Вашего профиля уже не существует'

    def random_joke(self, **kwargs):
        return self.joker.random_joke()

    def joke_by_phrase(self, phrase, **kwargs):
        return self.joker.get_joke_by_phrase(phrase)

    def subscribe(self, vk_id=None, phrase=None,
                  frequency=timedelta(hours=1), **kwargs):
        sub = Subscribe(subscriber=vk_id,
                        phrase=phrase,
                        frequency=frequency)
        sess = create_session()
        sess.add(sub)
        sess.commit()

    def unsubscribe(self, **kwargs):
        pass

    def do_command(self, *args, **kwargs):
        """
        Пустой метод, который должен использоваться в наследниках
        Как обработчик сообщений
        """
        pass