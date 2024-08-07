from typing import Any
from typing import Callable, Awaitable

from sqlalchemy import select, insert, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.adapter.sqlalchemy_db.models import Achievements


def create_achievement(
        session: AsyncSession
) -> Callable[..., Awaitable[Achievements]]:
    async def wrapper(
            *args: Any,
            **kwargs: Any
    ) -> Achievements:
        """
        Создать достижение.

        Пример запроса:
        INSERT INTO
            achievements (id, name, number_points, description)
        VALUES
            ($1, $2, $3, $4)
        """
        stmt = insert(Achievements).values(**kwargs).returning(Achievements)
        result = await session.execute(stmt)
        return result.scalar()

    return wrapper


def get_achievements(
        session: AsyncSession
) -> Callable[[int, int], Awaitable[ScalarResult[Achievements]]]:
    async def wrapper(limit: int, offset: int) -> ScalarResult[
        Achievements]:
        """
        Получить все достижения.

        SELECT
            a.id
            a.name,
            a.number_points,
            a.description
        FROM
            achievements AS a
        LIMIT
            $1
        OFFSET
            $2
        """
        stmt = select(Achievements).limit(limit).offset(offset)
        result = await session.execute(stmt)
        return result.scalars()

    return wrapper


def get_total_achievements(
        session: AsyncSession
) -> Callable[..., Awaitable[int]]:
    async def wrapper() -> int:
        """
        Получить количество достижений.

        SELECT
            COUNT(a.id)
        FROM
            achievements AS a
        """
        stmt = select(func.count(Achievements.id))
        return await session.scalar(stmt)

    return wrapper


def check_achievement(
        session: AsyncSession
) -> Callable[..., Awaitable[bool],]:
    async def wrapper(**kwargs: Any) -> bool:
        """
        Проверить наличия записи о достижении.

        SELECT EXISTS
            (SELECT
                a.id,
                a.name,
                a.number_points,
                a.description
             FROM
                achievements AS a
             WHERE
                a.name = $1
        """

        stmt = select(Achievements).filter_by(**kwargs).exists()
        return await session.scalar(select(stmt))

    return wrapper
