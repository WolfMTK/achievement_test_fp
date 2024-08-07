import uuid
from typing import Any, Callable, Awaitable

from app.domain.models import Achievements


def create_achievement(
        achievement_id: uuid.UUID
) -> Callable[..., Awaitable[Achievements]]:
    async def wrapper(*args: Any, **kwargs: Any) -> Achievements:
        return Achievements(
            id=achievement_id,
            name='test|тест',
            number_points=10,
            description='test|тест'
        )

    return wrapper


def get_achievements() -> Callable[[int, int], Awaitable[list[Achievements]]]:
    async def wrapper(
            limit: int,
            offset: int
    ) -> list[Achievements]:
        achievements = [
            Achievements(
                id=uuid.uuid4(),
                name='test|тест',
                number_points=10,
                description='test|тест'
            ),
            Achievements(
                id=uuid.uuid4(),
                name='test1|тест1',
                number_points=10,
                description='test1|тест1'
            ),
            Achievements(
                id=uuid.uuid4(),
                name='test2|тест2',
                number_points=10,
                description='test2|тест2'
            ),
            Achievements(
                id=uuid.uuid4(),
                name='test3|тест3',
                number_points=10,
                description='test3|тест3'
            )
        ]
        return achievements[offset:limit + offset]

    return wrapper


def get_total_achievements(total: int) -> Callable[..., Awaitable[int]]:
    async def wrapper() -> int:
        return total

    return wrapper


def check_achievement(
        is_check: bool
) -> Callable[..., Awaitable[bool]]:
    async def wrapper(*args: Any, **kwargs: Any) -> bool:
        return is_check

    return wrapper


def achievement_gateway_mock(
        is_check: bool = False
) -> dict[str, Any]:
    achievement_id = uuid.uuid4()
    total = 4
    return {
        'total': total,
        'achievement_id': achievement_id,
        'create_achievement': create_achievement(achievement_id),
        'get_achievements': get_achievements(),
        'get_total_achievements': get_total_achievements(total),
        'check_achievement': check_achievement(is_check)
    }
