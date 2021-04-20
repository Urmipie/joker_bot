import vk_api
from secret import VK_TOKEN
from random import randint


class VkSender:
    def __init__(self):
        self.vk_sess = vk_api.VkApi(token=VK_TOKEN)
        self.vk = self.vk_sess.get_api()

    def send_message(self, **kwargs):
        message = dict(random_id=randint(0, 2 ** 30), **kwargs)
        print(message)
        self.vk.messages.send(**message)
