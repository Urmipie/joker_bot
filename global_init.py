from data.users import User


if __name__ == '__main__':
    from data import db_session
    db_session.global_init('db/.db')
    sess = db_session.create_session()
    a = User(vk_id=2)
    sess.add(a)