import keyring
from vk_api import VkApi
from string import ascii_letters, digits
from random import choice


# Следующие 2 поля нужно заполнить перед запуском
SERVER_URL = 'https://e8894f41416e.ngrok.io'.strip() + '/vk_api'
VK_GROUP_ID = 191176862
VK_TOKEN = keyring.get_password('system', 'vk_token')

if not VK_TOKEN:
    raise IndexError("keyring didn't find the token")

vk_sess = VkApi(token=VK_TOKEN)
vk = vk_sess.get_api()


VK_CALLBACK_CONFIRMATION_CODE = vk.groups.getCallbackConfirmationCode(group_id=VK_GROUP_ID)['code']
VK_CALLBACK_SECRET_CODE = ''.join(choice(ascii_letters + digits) for _ in range(49))

del vk
del vk_sess
