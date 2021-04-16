import flask
from flask import Flask
from flask import request
from flask_vk_callback import VkCallbackAPI

app = Flask(__name__)
vk_callback = VkCallbackAPI(app, '/vk_api')
vk_callback.set_confirmation_code('a522c0d9')
vk_callback.secret_key = 'secret_code'


@vk_callback.unexpected_event()
def a():
    print(request.json)


if __name__ == '__main__':
    app.run()
