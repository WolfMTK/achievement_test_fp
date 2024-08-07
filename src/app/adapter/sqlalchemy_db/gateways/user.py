from typing import Any, Awaitable, Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.sqlalchemy_db.models import Users


def get_user(
        session: AsyncSession
) -> Callable[..., Awaitable[Users | None]]:
    async def wrapper(**kwargs: Any) -> Users | None:
        """
                Получить данные пользователя.

                SELECT
                    u.id,
                    u.name,
                    u.language
                FROM
                    users AS u
                WHERE
                    u.id = $1
                """
        stmt = select(Users).filter_by(**kwargs)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    return wrapper
