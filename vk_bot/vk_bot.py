from .vk_sender import VkSender
from actions import Action
from .vk_messages import VkMessage


class VkCommands(Action):
    def ok_keyboard(self, vk_id, keyboard_view, message=''):
        variants = ['cлучайный анекдот', 'анекдот по фразе', 'подписки', 'главное меню']
        keyboard = VkMessage('', variants)
        self.context[vk_id] = [variants, {variants[0]: self.random_joke,
                                          variants[1]: self.joke_by_phrase_message,
                                          variants[2]: None,    # TODO
                                          }, self.start_message]
        ans = keyboard.get(keyboard=keyboard_view)
        if message:
            ans['message'] = message + '\n' + ans['message']
        return ans

    def __init__(self, sender):
        super().__init__()

        self.commands = {
            'rnd': self.random_joke,
            'phrase': self.joke_by_phrase,

            'reg': self.new_user,
            'unreg': self.del_user,

            'start': self.start_message

        }

        self.message_without_context = {
            'старт': self.start_message,
            'помощь': None,
            'случайный анекдот': None,
            'начать': self.start_message,
            'меню': self.start_message
        }

        self.sender = sender
        self.context = {}
        # Хранит dict вида vk_id:
        # [<список ответов>, {<вариант ответа>: <действие>}, действие по умолчанию, Аргументы для функции]

    def do_command(self, command: str, message: dict, client_info: dict) -> dict:
        """
        Обработчик для команд
        :param command: команда
        :param message: сообщение
        :param client_info: словарь из callback api
        :return:
        """
        self.context[message['peer_id']] = [None, {}, None, None]  # очищает контекст, если вызвана конкретная команда
        args = command.split(' ')
        command = args.pop(0)
        action = self.commands.get(command)
        vk_id = message['peer_id']
        from_id = message['from_id']
        if action:
            ans = action(*args,
                         vk_id=vk_id,
                         from_id=from_id,
                         message=message,
                         context=self.context.setdefault(vk_id, [None, {}, None, None]),
                         client_info=client_info)
            return ans

    def new_message(self, obj: dict) -> dict:
        """
        Обработчик новых сообщений
        :param obj: вк-сообщение из callback vk: object
        :return:
        """
        message = obj['message']
        text = message['text'].lower()
        if text[0] in ('!', '/', '\\'):
            ans = self.do_command(command=text[1:], message=message, client_info=obj['client_info'])
        else:
            ans = self.do_message(message=message, client_info=obj['client_info'])

        if type(ans) == str:
            return dict(message=ans)
        elif type(ans) == dict:
            return ans
        else:
            return {'message': 'Я не понял вас'}

    def do_message(self, message: dict, client_info: dict):
        """
        Обработчик сообщений
        :param message:
        :param client_info:
        :return:
        """
        print(self.context)
        text = message['text'].lower()
        vk_id = message['peer_id']
        from_id = message['from_id']
        context = self.context.setdefault(vk_id, [None, {}, None, None])
        action = self.message_without_context.get(text)
        if not action:
            if text.isdigit():
                if int(text) >= len(context[0]):
                    return 'Нет такого варианта'
                action = context[1][context[0][int(text)].lower()]
            else:
                action = context[1].get(text.lower())
            if not action:
                try:
                    action = context[2]
                except IndexError:
                    action = None
        if action:
            ans = action(vk_id=vk_id,
                         from_id=from_id,
                         message=message,
                         client_info=client_info)
            return ans

    # Ниже сообщения

    def start_message(self, message: dict, client_info, vk_id, **kwargs):
        buttons = ['Зарегистрироваться', 'Случайный анекдот', 'Анекдот по фразе', 'Подписки']
        keys = VkMessage('Привет!', buttons)
        keyboard = client_info['keyboard']
        self.context[vk_id] = [list(map(str.lower, buttons)), {buttons[1].lower(): self.random_joke,
                                                               buttons[2].lower(): self.joke_by_phrase_message}, None]
        return keys.get(keyboard=keyboard)

    def joke_by_phrase_message(self, vk_id, **kwargs):
        self.context[vk_id] = [None, {}, self.get_text_message, self.joke_by_phrase]
        return 'Напиши тему'

    def get_text_message(self, message, vk_id, **kwargs):
        """Ловит текст и вызывает его в фунцию из context[3]
        :return: ответ функции """
        text = message['text'].lower()
        context = self.context[vk_id]
        self.context[vk_id] = [None, {}, self.start_message, context[3]]
        return context[3](text, message=message, vk_id=vk_id, **kwargs)

    def joke_by_phrase(self, phrase, client_info, vk_id, **kwargs):
        message = super(VkCommands, self).joke_by_phrase(phrase=phrase)
        return self.ok_keyboard(vk_id, client_info['keyboard'], message=message)


class VkBot:
    def __init__(self):
        self.sender = VkSender()
        self.commands = VkCommands(self.sender)

    def new_message(self, req: dict):
        obj = req['object']
        message = obj.get('message')
        out_message = dict(peer_id=message['peer_id'])
        obj = req['object']
        action = obj.get('action')
        if action:
            pass
        else:
            a = self.commands.new_message(obj=obj)
            out_message.update(a)

        if out_message.get('message') or out_message.get('keyboard'):
            print('vk: send:', out_message)
            print('con: ', self.commands.context)
            self.sender.send_message(**out_message)

    def new_user(self, user_id):
        pass

    def del_user(self, user_id):
        pass
