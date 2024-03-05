import uuid
from datetime import datetime
from typing import Optional, Type, TypeVar
from fastapi import HTTPException, status

from sqlalchemy import DateTime, String, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from db.meta import meta
T = TypeVar("T", bound="Base")

class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
    # id: Mapped[str] = mapped_column(
    #     String,
    #     primary_key=True,
    #     default=lambda _: str(uuid.uuid4()),
    #     unique=True,
    #     nullable=False,
    # )

    @classmethod
    async def get(cls: Type[T], session: AsyncSession, id_: str) -> Optional[T]:
        return await session.get(cls, id_)

    @classmethod
    async def get_or_404(cls: Type[T], session: AsyncSession, id_: str) -> T:
        if model := await cls.get(session, id_):
            return model
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{cls.__name__}[{id_}] not found"
            )

    async def save(self: T, session: AsyncSession) -> T:
        session.add(self)
        await session.flush()
        return self

    async def upsert(self : T, session: AsyncSession) -> T:
        await session.merge(self)
        await session.flush()
        return self
    
    async def delete(self: T, session: AsyncSession) -> None:
        await session.delete(self)