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
        :param vk_id: айдишник вк
        :return:
        """
        sess = create_session()
        print('new_user:\t', vk_id)
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
        print('del user:\t', vk_id)
        assert vk_id
        sess = create_session()
        user = sess.query(User).filter(User.vk_id == vk_id).first()
        if user:
            for subscribe in sess.query(Subscribe).filter(Subscribe.subscriber == vk_id).all():
                sess.delete(subscribe)
            for like in sess.query(Like).filter(Like.user_id == user.id).all():
                sess.delete(like)
            sess.delete(user)
            sess.commit()
            return 'Профиль успешно удалён'
        else:
            return 'Вашего профиля уже не существует'

    def random_joke(self, **kwargs):
        return self.joker.get_joke()

    def joke_by_phrase(self, phrase, **kwargs):
        return self.joker.get_joke(phrase)

    def subscribe(self, vk_id=None, phrase=None,
                  frequency=timedelta(hours=1), **kwargs):
        assert bool(vk_id), 'не передан айди'
        if len(self.get_subscribes(vk_id)) > 10:
            return 'У вас уже много подписок'
        sub = Subscribe(subscriber=vk_id,
                        phrase=phrase,
                        frequency=frequency)
        sess = create_session()
        sess.add(sub)
        sess.commit()
        return 'Добавлено'

    def get_subscribes(self, vk_id=None, **kwargs):
        sess = create_session()
        subscriber_id = sess.query(User).filter(User.vk_id == vk_id).first().vk_id
        return sess.query(Subscribe).filter(Subscribe.subscriber == subscriber_id).all()

    def get_formatted_subscribes(self, **kwargs):
        """
        возвращает список пар id шутки, текст для списка
        :param kwargs:
        :return:
        """
        subs_list = self.get_subscribes(**kwargs)
        for i, subscribe in enumerate(subs_list):
            subs_list[i] = (subscribe.id, f'{i}) '
                                          f'{f"Тема {subscribe.phrase}" if subscribe.phrase else "Случайная"}, '
                                          f'каждые {subscribe.frequency.seconds // 60} минут')
        return subs_list

    def unsubscribe(self, subscribe_id, **kwargs):
        sess = create_session()
        sub = sess.query(Subscribe).filter(Subscribe.id == subscribe_id).first()
        sess.delete(sub)
        sess.commit()
        return 'Вы отписались'

    def do_command(self, *args, **kwargs):
        """
        Пустой метод, который должен использоваться в наследниках
        Как обработчик сообщений
        """
        pass
