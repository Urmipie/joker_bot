# unexpected event: message_deny
a = dict(type='message_deny', object={'user_id': 232266268}, group_id=191176862,
         event_id='164483eefb417caa26dbfb598de44f0abe2d9f1a', secret='secret_code')

# unexpected event: message_allow
a = dict(type='message_allow', object={'user_id': 232266268, 'key': ''}, group_id=191176862,
         event_id='917d5fbd06c42b4b7d69fd8b061f4f6880955b8e', secret='secret_code')

# unexpected event: message_new
a = dict(type='message_new',
         object={'id': 34, 'date': 1618846428, 'out': 0, 'user_id': 232266268, 'read_state': 0, 'title': '',
                 'body': 'П',
                 'owner_ids': []}, group_id=191176862, event_id='1c6fc79d464b34d6995982b0c1e10136f1b66bed',
         secret='secret_code')

# Добавление в беседу
a = dict(
    type='message_new',
    object={
        'message': {'date': 1618848393,
                    'from_id': 232266268,
                    'id': 0,
                    'out': 0,
                    'peer_id': 2000000002,
                    'text': '',
                    'conversation_message_id': 90,
                    'action': {'type': 'chat_invite_user',
                               'member_id': -191176862},
                    'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False},
        'client_info': {
            'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'callback', 'intent_subscribe',
                               'intent_unsubscribe'], 'keyboard': True, 'inline_keyboard': True, 'carousel': False,
            'lang_id': 0}},
    group_id=191176862,
    event_id='1f6c56febee9c751b0cafdd1b16a7ffb2cd8b9c3', secret='secret_code')

# Сообщение в беседе
a = dict(type='message_new',
         object={
             'message': {'date': 1618848641,
                         'from_id': 232266268,
                         'id': 0,
                         'out': 0,
                         'peer_id': 2000000002,
                         'text': '[club191176862|@testingmybot], про',
                         'conversation_message_id': 94,
                         'fwd_messages': [],
                         'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False},
             'client_info': {
                 'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'callback',
                                    'intent_subscribe',
                                    'intent_unsubscribe'], 'keyboard': True, 'inline_keyboard': True, 'carousel': False,
                 'lang_id': 0}},
         group_id=191176862,
         event_id='bfb4f881e8a8777c5cb0f30af9c0bac33a61a717',
         secret='secret_code')
