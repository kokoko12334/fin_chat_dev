from settings import settings
# DB session 연결

from db.connection import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from Services.dependencies import save_signals
import asyncio
from utils.db_infos import init_pinecone
from db.SSH_connection import SSHConnection

def create_async_session(ssh: SSHConnection):
    engine = create_engine(ssh)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    session = session_factory()
    return session
    
async def cron_job(ssh: SSHConnection):
    init_pinecone()
    session = create_async_session(ssh)
    await save_signals(session)
    await session.commit()
    

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    ssh = SSHConnection()
    loop.run_until_complete(cron_job(ssh))
    # try: 
    #     loop.run_until_complete(cron_job(ssh))
    # finally:
    #     loop.close()
    
    # loop.close()
    # asyncio.set_event_loop(loop)
    # asyncio.run(cron_job())