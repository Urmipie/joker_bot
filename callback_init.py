from vk_api.vk_api import VkApiMethod
from random import randrange



def callback_init(group_id: int, server_id: int, url: str, secret_key: str, vk_sess: VkApiMethod):
    vk = vk_sess.get_api()
    title = f'joker_bot_{randrange(1, 100)}'
    print('VkCallback server title:', title)
    vk.groups.editCallbackServer(group_id=group_id,
                                 server_id=server_id,
                                 url=url,
                                 title=title,
                                 secret_key=secret_key)
