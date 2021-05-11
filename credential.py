from os import environ as env
from vk_api import VkApi
from string import ascii_letters, digits
from random import choice


# Вариант для Heroku
SERVER_PORT = int(env.get("PORT", 5000))
SERVER_URL = 'https://yandexvkproj.herokuapp.com' + '/vk_api'
VK_GROUP_ID = 191176862

# Пришлось чуть-чуть помудрить с передачей токена для Heroku. Нужно создать vk_token.txt с токеном

with open('vk_token.txt') as file:
    VK_TOKEN = file.read().strip()

if not VK_TOKEN:
    raise IndexError("Токена нема")

vk_sess = VkApi(token=VK_TOKEN)
vk = vk_sess.get_api()


VK_CALLBACK_CONFIRMATION_CODE = vk.groups.getCallbackConfirmationCode(group_id=VK_GROUP_ID)['code']
VK_CALLBACK_SECRET_CODE = ''.join(choice(ascii_letters + digits) for _ in range(49))

del vk
del vk_sess
