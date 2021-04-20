import secret
import flask
from flask import Flask
from flask import request
from flask_vk_callback import VkCallbackAPI
from vk_bot.vk_bot import VkBot
import data

app = Flask(__name__)
vk_callback = VkCallbackAPI(app, '/vk_api')
vk_callback.set_confirmation_code(secret.VK_CALLBACK_CONFIRMATION_CODE)
vk_callback.secret_key = secret.VK_CALLBACK_SECRET_CODE
vk_bot = VkBot()


@vk_callback.event('message_allow')
def new_user():
    print(request.json)
    vk_bot.new_user(request.json['object']['user_id'])


@vk_callback.event('message_deny')
def del_user():
    print(request.json)
    vk_bot.del_user(request.json['object']['user_id'])


@vk_callback.event('message_new')
def new_message():
    print(request.json)
    vk_bot.new_message(request.json)


@vk_callback.unexpected_event()
def unexpected_event():
    print(f'unexpected event: {request.json["type"]}\n{request.json}')


if __name__ == '__main__':
    app.run()
