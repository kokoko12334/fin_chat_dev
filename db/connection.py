from settings import settings
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from db.SSH_connection import SSHConnection


def async_ssh_create_engine(ssh: SSHConnection) -> AsyncEngine:
    DATABASE_URL = f"mysql+aiomysql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@127.0.0.1:{ssh.tunnel.local_bind_port}/{settings.DATABASE_NAME}"
    return create_async_engine(DATABASE_URL, echo=True)

def async_create_engine() -> AsyncEngine:
    return create_async_engine(settings.DATABASE_URL, echo=True)

def create_engine(ssh: SSHConnection) -> AsyncEngine:
    # print(settings.need_ssh)
    if settings.need_ssh:
        ssh.connect()
        return async_ssh_create_engine(ssh)
    else:
        return async_create_engine()
    
def create_async_session(engine: AsyncEngine):
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    session = session_factory()
    return session

def _setup_db(app: FastAPI,ssh: SSHConnection) -> None:  # pragma: no cover
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_engine(ssh)
    # ssh.connect()
    # engine = async_ssh_create_engine(ssh)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory
