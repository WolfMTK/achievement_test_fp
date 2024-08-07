import datetime as dt
import uuid
from typing import Any, Callable, Awaitable

from app.domain.enums import Language
from app.domain.models import (
    UsersAchievements,
    UserId,
    AchievementId,
    Achievements,
    Users,
)


def create_achievement_user(
        user_id: uuid.UUID,
        achievement_id: uuid.UUID,
        date_on: dt.datetime
) -> Callable[..., Awaitable[UsersAchievements]]:
    async def wrapper(*args: Any, **kwargs: Any) -> UsersAchievements:
        return UsersAchievements(
            user_id=user_id,
            achievement_id=achievement_id,
            date_on=date_on,
            achievement=None,
            user=None
        )

    return wrapper


def get_achievements_user(
        _user_id: uuid.UUID,
        achievement_id: uuid.UUID,
        date_on: dt.datetime,
) -> Callable[[UserId, int, int], Awaitable[list[UsersAchievements]]]:
    async def wrapper(
            user_id: UserId,
            limit: int,
            offset: int
    ) -> list[UsersAchievements]:
        users_achievements = [
            UsersAchievements(
                user_id=_user_id,
                achievement_id=achievement_id,
                date_on=date_on,
                achievement=Achievements(
                    id=achievement_id,
                    name='тест|test',
                    number_points=10,
                    description='тест|test'
                ),
                user=Users(
                    id=_user_id,
                    name='test',
                    language='RU'
                )
            ),
            UsersAchievements(
                user_id=_user_id,
                achievement_id=achievement_id,
                date_on=date_on,
                achievement=Achievements(
                    id=achievement_id,
                    name='тест|test',
                    number_points=10,
                    description='тест|test'
                ),
                user=Users(
                    id=_user_id,
                    name='test',
                    language='RU'
                )
            )
        ]
        return users_achievements

    return wrapper


def check_user_id_and_achievement_id(
        is_user_id_and_achievement_id: bool
) -> Callable[[UserId, AchievementId], Awaitable[bool]]:
    async def wrapper(
            user_id: UserId,
            achievement_id: AchievementId
    ) -> bool:
        return is_user_id_and_achievement_id

    return wrapper


def check_achievement_user(
        is_achievement_user: bool
) -> Callable[[UserId, AchievementId], Awaitable[bool]]:
    async def wrapper(
            user_id: UserId,
            achievement_id: AchievementId
    ) -> bool:
        return is_achievement_user

    return wrapper


def get_total_achievements_user(
        total: int
) -> Callable[[UserId], Awaitable[int]]:
    async def wrapper(user_id: UserId) -> int:
        return total

    return wrapper


def get_max_achievement_points_user(
        is_max_achievement_points: bool,
        user_id: uuid.UUID
) -> Callable[..., Awaitable[tuple[UserId, str, int] | None]]:
    async def wrapper() -> tuple[UserId, str, int] | None:
        if is_max_achievement_points:
            return (user_id, 'test', 10)
        return None

    return wrapper


def check_user_exists(
        is_user_exists: bool
) -> Callable[[UserId], Awaitable[bool]]:
    async def wrapper(user_id: UserId) -> bool:
        return is_user_exists

    return wrapper


def get_max_achievements_user(
        is_max_achievements_user: bool,
        user_id: UserId
) -> Callable[..., Awaitable[tuple[UserId, str, int] | None]]:
    async def wrapper() -> tuple[UserId, str, int] | None:
        if is_max_achievements_user:
            return (user_id, 'test', 10)
        return None

    return wrapper


def get_users_with_days_streak(
        user_id: uuid.UUID
) -> Callable[..., Awaitable[list[Users]]]:
    async def wrapper() -> list[Users]:
        users = [
            Users(
                id=user_id,
                name='test',
                language=Language.RU
            ),
            Users(
                id=uuid.uuid4(),
                name='test',
                language=Language.RU
            )
        ]
        return users

    return wrapper


def get_users_with_min_points_diff(
        is_user_with_min_points_diff: bool,
        user_id: uuid.UUID
) -> Callable[..., Awaitable[list[tuple[UserId, str, int, int]] | None]]:
    async def wrapper() -> list[tuple[UserId, str, int, int]] | None:
        if is_user_with_min_points_diff:
            return [
                (user_id, 'test', 1250, 90),
                (uuid.uuid4(), 'test', 1160, 90)
            ]
        return None

    return wrapper


def get_users_with_max_points_diff(
        is_user_with_max_points_diff: bool,
        user_id: uuid.UUID
) -> Callable[..., Awaitable[list[tuple[UserId, str, int, int]] | None]]:
    async def wrapper() -> list[tuple[UserId, str, int, int]] | None:
        if is_user_with_max_points_diff:
            return [
                (user_id, 'test', 1250, 90),
                (uuid.uuid4(), 'test', 1160, 90)
            ]
        return None

    return wrapper


def achievement_user_gateway_mock(
        is_user_exists: bool = True,
        is_achievement_user: bool = False,
        is_max_achievement_points: bool = True,
        is_user_id_and_achievement_id: bool = True,
        is_max_achievements_user: bool = True,
        is_user_with_max_points_diff: bool = True,
        is_user_with_min_points_diff: bool = True
) -> dict[str, Any]:
    date_on = dt.datetime.now()
    user_id = uuid.uuid4()
    achievement_id = uuid.uuid4()
    total = 2
    return {
        'date_on': date_on,
        'user_id': user_id,
        'achievement_id': achievement_id,
        'total': total,
        'create_achievement_user': create_achievement_user(
            user_id,
            achievement_id, date_on
        ),
        'get_achievements_user': get_achievements_user(
            user_id,
            achievement_id,
            date_on
        ),
        'check_user_id_and_achievement_id':
            check_user_id_and_achievement_id(is_user_id_and_achievement_id),
        'check_achievement_user': check_achievement_user(is_achievement_user),
        'get_total_achievements_user': get_total_achievements_user(total),
        'get_max_achievement_points_user': get_max_achievement_points_user(
            is_max_achievement_points, user_id
        ),
        'check_user_exists': check_user_exists(is_user_exists),
        'get_max_achievements_user': get_max_achievements_user(
            is_max_achievements_user, user_id
        ),
        'get_users_with_days_streak': get_users_with_days_streak(user_id),
        'get_users_with_min_points_diff': get_users_with_min_points_diff(
            is_user_with_min_points_diff,
            user_id
        ),
        'get_users_with_max_points_diff': get_users_with_max_points_diff(
            is_user_with_max_points_diff,
            user_id
        )
    }
