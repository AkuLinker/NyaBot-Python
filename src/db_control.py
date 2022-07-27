from sqlalchemy import select

from db import AsyncSessionLocal, User
from loger import log


async def get_user(telegram_id: int, session: AsyncSessionLocal) -> User:
    """Returns user's instance"""
    user = await session.execute(
        select(User).where(
            User.telegram_id == telegram_id
        )
    )
    user = user.scalars().first()
    return user


async def registration(telegram_id: int) -> None:
    """Registers user"""
    user = User(telegram_id=telegram_id)
    async with AsyncSessionLocal() as session:
        session.add(user)
        await session.commit()


async def user_check(telegram_id: int) -> bool:
    """Returns registrtion status of user"""
    async with AsyncSessionLocal() as session:
        user = await get_user(telegram_id, session)
    if user:
        return True
    return False


async def check_language(telegram_id: int, const: dict[str, str]) -> str:
    """Returns constant in user's language"""
    async with AsyncSessionLocal() as session:
        user = await get_user(telegram_id, session)
    return const[user.language]


async def check_nsfw(telegram_id: int) -> bool:
    """Returns user's nsfw preference"""
    async with AsyncSessionLocal() as session:
        user = await get_user(telegram_id, session)
    return user.nsfw_is_ok


async def change_language_db(telegram_id: int, lang: str) -> None:
    """Changes user's language"""
    async with AsyncSessionLocal() as session:
        user = await get_user(telegram_id, session)
        user.language = lang
        session.add(user)
        await session.commit()


async def change_nsfw_db(telegram_id: int, nsfw: bool) -> None:
    """Changes user's nsfw settings"""
    async with AsyncSessionLocal() as session:
        user = await get_user(telegram_id, session)
        user.nsfw_is_ok = nsfw
        session.add(user)
        await session.commit()
