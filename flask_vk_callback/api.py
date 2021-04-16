import flask


class VkCallbackAPI:
    @staticmethod
    def ok_decorated_func(func):
        """
        Декоратор - заглушка, который возвращает положительный ответ на любой запрос
        :return:
        """
        def decorated(*args, **kwargs):
            func(*args, **kwargs)
            return flask.make_response('ok', 200)
        return decorated

    def __init__(self, app: flask.Flask, url: str):
        self.app = app
        self.confirmation_code = None
        self._unexpected_event_action = None
        self.secret_key = None
        self.app.add_url_rule(url, view_func=self.event_handler, methods=['POST', ])
        self.actions = {}

    def set_confirmation_code(self, code: str):
        """
        Устанавливает ответ на запрос с типом "confirmation" функции _confirmation
        которая отвечает кодом
        :param code: Код подтверждения
        """
        self.confirmation_code = code
        self.actions['confirmation'] = self._confirmation

    def event_handler(self):
        """
        Ловит запросы на сервер
        """
        if flask.request.json:
            if flask.request.json.get('secret', None) != self.secret_key:
                return flask.make_response('Wrong secret code', 401)

            req_type = flask.request.json.get('type', False)
            if req_type:
                f = self.actions.get(req_type, self._unexpected_event_action)
                if f:
                    ans = f()
                    return ans
        return flask.make_response('You are not expected here', 400)

    def add_action(self, method: str, func):
        """
        Добавляет ответ на тип события. При отправке на сервер этого type будет вызвана funct
        :param method: название метода
        :param func: функция, которая будет выполняться
        """
        self.actions[method] = func

    def event(self, method: str):
        """
        То же, что и add_action, но декоратор
        :param method: название метода
        """
        def decorator(func):
            func = self.ok_decorated_func(func)
            self.add_action(method, func)
            return func
        return decorator

    def unexpected_event(self):
        """
        Декоратор, который вызывает функцию, если не задана отдельная для работы с типом события
        """
        def decorator(func):
            func = self.ok_decorated_func(func)
            self._unexpected_event_action = func
            return func
        return decorator

    def _confirmation(self):
        """
        функция, задаваемая set_confirmation_code и вызываемая при авторизации
        """
        if self.confirmation_code:
            return flask.make_response(self.confirmation_code, 200)
        else:
            raise NameError('confirmation code not specified')