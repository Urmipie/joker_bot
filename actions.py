from jokes.Joker import Joker
from data.db_session import create_session
from data.users import User


class Action:
    def __init__(self):
        self.joker = Joker()

    def new_user(self, **kwargs):
        """

        :param kwargs: vk_id - айдишник вк
        :return:
        """
        sess = create_session()
        sess.add(User(**kwargs))

    def del_user(self):
        pass

    def random_joke(self):
        return self.joker.random_joke()

    def joke_by_phrase(self, phrase):
        return self.joker.get_joke_by_phrase(phrase)

    def subscribe(self):
        pass

    def unsubscribe(self):
        pass

    def do(self, *args, **kwargs):
        """
        Пустой метод, который должен использоваться в наследниках
        Как обработчик сообщений
        """
        pass
