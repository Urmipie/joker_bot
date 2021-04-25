import keyring


VK_CALLBACK_CONFIRMATION_CODE = '5bb66ea6'
VK_CALLBACK_SECRET_CODE = 'secret_code'
VK_TOKEN = keyring.get_password('system', 'vk_token')
if not VK_TOKEN:
    raise IndexError("keyring didn't find the token")
