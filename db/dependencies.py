from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from starlette.requests import Request

async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session = request.app.state.db_session_factory()
    try:
        yield session
        await session.commit()
    finally:
        session.close()