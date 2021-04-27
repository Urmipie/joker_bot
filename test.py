from data.db_session import global_init, create_session
from data.users import User


global_init('test.db')
sess = create_session()
sess.add(User(vk_id=21))
sess.commit()
