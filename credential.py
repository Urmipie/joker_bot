import keyring
from vk_api_init import VkApi
from string import ascii_letters, digits
from random import choice


# Следующие 2 поля нужно заполнить перед запуском
SERVER_URL = 'http://3bd05bac4b03.ngrok.io'.strip() + '/vk_api'
GROUP_ID = 191176862
VK_TOKEN = keyring.get_password('system', 'vk_token')

if not VK_TOKEN:
    raise IndexError("keyring didn't find the token")

vk_sess = VkApi(token=VK_TOKEN)
vk = vk_sess.get_api()


VK_CALLBACK_CONFIRMATION_CODE = vk.groups.getCallbackConfirmationCode(group_id=GROUP_ID)['code']
VK_CALLBACK_SECRET_CODE = ''.join(choice(ascii_letters + digits) for _ in range(49))

del vk
del vk_sess
