import asyncio
from datetime import datetime
from data.db_session import create_session
from data.subscribes import Subscribe
from data.users import User


async def subscribe_send():
    while True:
        sess = create_session()
        sess.query(Subscribe).filter(Subscribe.next_send <= datetime.now())
        sess.close()
        await asyncio.sleep(60 * 30)
