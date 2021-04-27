from vk_api_init import VK
from credential import VK_TOKEN
from random import randint


class VkSender:
    @staticmethod
    def send_message(**kwargs):
        message = dict(random_id=randint(0, 2 ** 30), **kwargs)
        message.setdefault('keyboard', None)
        VK.messages.send(**message)