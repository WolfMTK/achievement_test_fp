from typing import Callable, Any

from app.application.commands import get_achievements
from app.application.dto import GetAchievementListDTO, Pagination


async def test_get_achievements(
        achievement_gateway: Callable[..., dict[str, Any]],
) -> None:
    gateway = achievement_gateway()
    limit = 10
    offset = 0
    data = GetAchievementListDTO(
        Pagination(
            limit=limit,
            offset=offset
        )
    )
    data = await get_achievements(gateway, data)
    assert limit == data.limit
    assert offset == data.offset
    assert gateway['total'] == data.total
    assert len(data.achievements) == data.total
