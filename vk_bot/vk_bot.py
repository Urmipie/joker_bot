from flask import request
# import vk_comands
# import vk_actions
from .vk_sender import VkSender
from actions import Action


class VkActions(Action):
    def __init__(self):
        super().__init__()


class VkCommands(Action):
    def __init__(self):
        super().__init__()
        self.commands = {
            'rnd': self.random_joke,
            'phrase': self.joke_by_phrase
        }

    def do(self, command: str):
        args = command[1:].split(' ')
        command = args.pop(0)
        action = self.commands.get(command)
        if action:
            try:
                ans = action(*args)
                return ans
            except Exception as error:
                return f'Ошибка: {error}'


class VkBot:
    def __init__(self):
        self.sender = VkSender()
        self.commands = VkCommands()

    def new_message(self, req: dict):
        obj = req['object']
        obj_msg = obj['message']
        message = dict(peer_id=obj['message']['peer_id'])
        obj = req['object']
        action = obj.get('action')
        if action:
            """res = vk_actions.action(req, action)
            return res"""
            pass
        else:
            text = obj_msg['text']
            if text[0] in ('/', '!', '\\'):
                message['message'] = self.commands.do(text)

        if message['message']:
            print('vk: send:', message)
            self.sender.send_message(**message)


    def new_user(self, user_id):
        pass

    def del_user(self, user_id):
        pass