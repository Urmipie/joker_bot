import keyring

a = keyring.get_password('system', 'username')
print(a)