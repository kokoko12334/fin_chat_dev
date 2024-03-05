from db.connection import *
import asyncio
from sqlalchemy import text
from db.SSH_connection import SSHConnection



async def main():
    async with engine.connect() as conn:
        query = "SELECT * FROM tbs_trading_signal_log"
        result = await conn.execute(text(query))
        rows = result.fetchall()
        for row in rows:
            print(row)


ssh = SSHConnection()
ssh.connect()
engine = async_ssh_create_engine(ssh)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
ssh.disconnect()
loop.close