"""def bot_invited(req):
    if abs(req['object']['action']['member_id']) == req['group_id']:
        return dict(message='Привет!\nЯ шутник-бот, вот мои возможности:')
    else:
        return dict(message=f"Привет, некто под id {abs(req['object']['action']['member_id'])}")


actions = {
    'chat_invite_user': bot_invited
}


def action(req, action):
    action = actions.get(action)
    if action:
        return action(req)
    else:
        return"""


class VkAction:
    def __init__(self, actions):
        self.actions = actions