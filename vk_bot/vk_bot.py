from .vk_sender import VkSender
from actions import Action
from .vk_messages import VkMessage
from datetime import timedelta
from credential import GROUP_ID
from vk_api_init import VK

class VkCommands(Action):
    def ok_keyboard(self, vk_id, keyboard_view, message=''):
        variants = ['cлучайный анекдот', 'анекдот по фразе', 'отписаться', 'новая подписка', 'главное меню']
        keyboard = VkMessage(message, variants)
        self.context[vk_id] = [variants, {variants[0]: self.random_joke,
                                          variants[1]: self.joke_by_phrase_message,
                                          variants[2]: self.unsubscribe_first_message,
                                          variants[3]: self.subscribe_first_message
                                          }, self.start_message]
        ans = keyboard.get(keyboard=keyboard_view)
        return ans

    def __init__(self, sender):
        super().__init__()

        self.commands = {
            'rnd': self.random_joke,
            'phrase': self.joke_by_phrase,

            'reg': self.new_user,
            'unreg': self.del_user,

            'start': self.start_message,
            'старт': self.start_message

        }

        self.message_without_context = {
            'старт': self.start_message,
            'помощь': None,
            'случайный анекдот': self.random_joke,
            'новая подписка': self.subscribe_first_message,

            'начать': self.start_message,
            'меню': self.start_message,
            'главное меню': self.start_message
        }

        self.sender = sender
        self.context = {}
        # Хранит dict вида
        # vk_id: [<список ответов>, {<вариант ответа>: <действие>},
        # действие по умолчанию, Аргументы для функции дефолтного действия
        # , {<доп.информация, наличие не гарантируется>}]

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
        context = self.context.setdefault(vk_id, [None, {}, None, None, {}])
        action = self.message_without_context.get(text)
        if not action:
            if context[2] == self.get_text_from_message:
                action = context[2]
            elif text.isdigit():
                if int(text) >= len(context[0]):
                    return 'Нет такого варианта'
                action = context[1].get(context[int(text)])
            else:
                action = context[1].get(text.lower())
            if not action:
                action = context[2]
        if action:
            print(vk_id, 'goto', action)
            ans = action(vk_id=vk_id,
                         from_id=from_id,
                         message=message,
                         client_info=client_info)
            return ans

    # Ниже сообщения

    def get_text_from_message(self, message, vk_id, **kwargs):
        """Ловит текст и вызывает фунцию из context[3], передавая первым параметром текст
        :return: ответ функции """
        text = message['text'].lower()
        context = self.context[vk_id]
        return context[3](text, message=message, vk_id=vk_id, **kwargs)

    def start_message(self, client_info, vk_id, **kwargs):
        return self.ok_keyboard(vk_id, keyboard_view=client_info['keyboard'], message='')

    def joke_by_phrase_message(self, vk_id, **kwargs):
        self.context[vk_id] = [None, {}, self.get_text_from_message, self.joke_by_phrase]
        return 'Напиши тему'

    def joke_by_phrase(self, phrase, client_info, vk_id, **kwargs):
        super(VkCommands, self).joke_by_phrase(phrase=phrase)
        return self.ok_keyboard(vk_id, client_info['keyboard'], message='Подписка добавлена!')

    def subscribe_first_message(self, vk_id, **kwargs):
        self.context[vk_id] = [None, {}, self.get_text_from_message, self.subscribe_second_message]
        return 'Раз в сколько минут нужно отправлять?'

    def subscribe_second_message(self, frequency, vk_id, client_info, **kwargs):
        print('frequency', frequency)
        buttons = ['главное меню', 'без темы']
        try:
            frequency = int(frequency)
            if frequency <= 0:
                raise ValueError
        except ValueError:
            return 'Нужно целое положительное число, а не вот это вот'
        self.context[vk_id] = [None,
                               {
                                   buttons[0]: self.start_message,
                                   buttons[1]: self.subscribe_third_message
                               },
                               self.get_text_from_message,
                               self.subscribe_third_message,
                               {'new_subscribe': dict(
                                   frequency=frequency
                               )}]
        message = VkMessage('Введите тему', buttons, inline=True)
        print('1ssss', self.context[vk_id])
        return message.get(keyboard=client_info['keyboard'])

    def subscribe_third_message(self, phrase=None, vk_id=None, client_info=None, **kwargs):
        print('ssss', self.context[vk_id])
        assert bool(vk_id), 'Это невозможно, но vk_id не передан'
        if not phrase or phrase == 'без темы':
            phrase = ''
        ans = self.subscribe(vk_id=vk_id, phrase=phrase,
                             frequency=timedelta(minutes=self.context[vk_id][4]['new_subscribe']['frequency']))
        return self.ok_keyboard(vk_id, keyboard_view=client_info['keyboard'], message=ans)

    def unsubscribe_first_message(self, vk_id, client_info,**kwargs):
        sub_list = self.get_formatted_subscribes(vk_id=vk_id)
        if not sub_list:
            return self.ok_keyboard(vk_id=vk_id, keyboard_view=client_info['keyboard'], message='У вас нет подписок')
        names = []
        ids = []
        for sub in sub_list:
            i_id, i_name = sub
            ids.append(i_id)
            names.append(i_name)
        message = VkMessage('Какую подписку удалить:', names + ['главное меню'], inline=True)
        self.context[vk_id] = [None, {}, self.get_text_from_message, self.unsubscribe_second_message, {'ids': ids}]
        return message.get(keyboard=client_info['keyboard'])

    def unsubscribe_second_message(self, text, vk_id, client_info, **kwargs):
        num = text.split(')')[0]
        try:
            sub_id = self.context[vk_id][4]['ids'][int(num)]
        except IndexError or TypeError:
            message = VkMessage('Я вас не понял', ['главное меню'])
            return message.get(keyboard=True)
        ans = self.unsubscribe(subscribe_id=sub_id)
        return self.ok_keyboard(vk_id=vk_id, keyboard_view=client_info['keyboard'], message=ans)

    def help(self, ):
        pass



class VkBot:
    def __init__(self):
        self.sender = VkSender()
        self.commands = VkCommands(self.sender)

    def new_message(self, req: dict):
        obj = req['object']
        message = obj.get('message')
        out_message = dict(peer_id=message['peer_id'])
        obj = req['object']
        action = message.get('action')
        a = {}
        if action:
            action_type = action['type']
            if action_type in ('chat_invite_user', 'message_allow'):
                if action_type == 'chat_invite_user' and not action['member_id'] == GROUP_ID:
                    print('ignore')
                    return

                a = self.commands.start_message(message=message, client_info=obj['client_info'])
                self.commands.new_user(vk_id=message['peer_id'])

            elif action_type in ('message_deny', 'chat_kick_user'):
                if action_type == 'chat_kick_user' and not action['member_id'] == GROUP_ID:
                    print('ignore')
                    return

                self.commands.del_user(vk_id=message['peer_id'])
        else:
            a = self.commands.new_message(obj=obj)

        out_message.update(a)
        if out_message.get('message') or out_message.get('keyboard'):
            print('vk: send:', out_message)
            print('con: ', self.commands.context)
            self.sender.send_message(**out_message)
