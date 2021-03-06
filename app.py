"""
Этот файл нельзя запускать через специальное фласк-окружение, которое предлагает PyCharm,
Т.К. Почему-то ломается flask_apscheduler
"""


from credential import VK_GROUP_ID, VK_TOKEN, VK_CALLBACK_CONFIRMATION_CODE, VK_CALLBACK_SECRET_CODE
from credential import SERVER_URL, SERVER_PORT
import flask
from flask_apscheduler import APScheduler
from flask import Flask
from flask import request
from flask_vk_callback import VkCallbackAPI
from vk_bot.vk_bot import VkBot
from data import db_session
from callback_init import callback_init
from vk_api_init import VK


db_session.global_init('db/.db')

app = Flask(__name__)


scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)

vk_callback = VkCallbackAPI(app, '/vk_api')
vk_callback.set_confirmation_code(VK_CALLBACK_CONFIRMATION_CODE)
vk_callback.secret_key = VK_CALLBACK_SECRET_CODE
callback_init(group_id=VK_GROUP_ID, server_id=2, url=SERVER_URL,
              secret_key=VK_CALLBACK_SECRET_CODE, vk=VK)
vk_bot = VkBot()


@scheduler.task("interval", id="vk_distribution", seconds=1, misfire_grace_time=900)
def distribution():
    vk_bot.distribution()


@vk_callback.event('message_allow')
def new_user():
    print(request.json)
    vk_bot.new_user(vk_id=request.json['object']['user_id'])


@vk_callback.event('message_deny')
def del_user():
    print(request.json)
    vk_bot.del_user(vk_id=request.json['object']['user_id'])


@vk_callback.event('message_new')
def new_message():
    # event_type = flask.request.json.get('type', False)
    print(request.json)
    vk_bot.new_message(request.json)


@vk_callback.unexpected_event()
def unexpected_event():
    print(f'unexpected event: {request.json["type"]}\n{request.json}')


if __name__ == '__main__':
    scheduler.start()
    app.run()
