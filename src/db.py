from sqlalchemy import Column, Integer, Boolean, Enum
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from sqlalchemy.sql import expression

from constants import LANGUAGES


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


class User(Base):
    telegram_id = Column(Integer, unique=True, nullable=False)
    nsfw_is_ok = Column(
        Boolean, nullable=False, server_default=expression.false()
    )
    language = Column(
        Enum(*LANGUAGES), nullable=False, server_default='english'
    )


engine = create_async_engine('sqlite+aiosqlite:///sqlite.db')

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
