from .vk_sender import VkSender
from actions import Action
from .vk_messages import VkMessage, START_MESSAGE


class VkCommands(Action):
    def __init__(self, sender):
        super().__init__()

        self.commands = {
            'rnd': self.random_joke,
            'phrase': self.joke_by_phrase,

            'reg': self.new_user,
            'unreg': self.del_user,

            'start': self.start

        }

        self.message_without_context = {
            'старт': self.start,
            'помощь': None,
            'случайный анекдот': None,
            'начать': self.start
        }

        self.sender = sender
        self.context = {}  # Хранит dict вида vk_id: [<список ответов>, {<вариант ответа>: <действие>}]

    def do_command(self, command: str, message: dict, client_info: dict) -> dict:
        self.context[message['peer_id']] = {}  # очищает контекст, если вызвана конкретная команда
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
                         context=self.context.setdefault(vk_id, {}),
                         client_info=client_info)
            if type(ans) == str:
                return dict(message=ans)
            elif type(ans) == dict:
                return ans
            else:
                raise ValueError(f'Expect dict or str, got {type(ans)}')

    def start(self, *args, message: dict, client_info, context, vk_id, **kwargs):
        buttons = ['Зарегистрироваться', 'Случайный анекдот', 'Анекдот по фразе', 'Подписки']
        keys = VkMessage('Привет!', buttons)
        keyboard = client_info['keyboard']
        self.context[vk_id] = [list(map(str.lower, buttons)), {buttons[1].lower(): self.random_joke}]
        return keys.get(keyboard=keyboard)

    def new_message(self, obj: dict) -> dict:
        """
        Обработчик новых сообщений
        :param obj: вк-сообщение из callback vk: object
        :return:
        """
        message = obj['message']
        text = message['text'].lower()
        if text[0] in ('!', '/', '\\'):
            return self.do_command(command=text[1:], message=message, client_info=obj['client_info'])
        else:
            return self.do_message(message=message, client_info=obj['client_info'])

    def do_message(self, message: dict, client_info: dict):
        text = message['text'].lower()
        vk_id = message['peer_id']
        from_id = message['from_id']
        context = self.context.setdefault(vk_id, {})
        action = self.message_without_context.get(text)
        print('context', context)
        print('text: ', text)
        if not action:
            if text.isdigit():
                if int(text) >= len(context[0]):
                    return 'Нет такого варианта'
                action = context[1][context[0][int(text)].lower()]
            else:
                action = context[1].get(text.lower())
        ans = None
        if action:
            ans = action(vk_id=vk_id,
                         from_id=from_id,
                         message=message,
                         context=context,
                         client_info=client_info)
            print('ans:', ans)
        if type(ans) == str:
            return dict(message=ans)
        elif type(ans) == dict:
            return ans
        else:
            return dict(message='Не понял тебя')



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
