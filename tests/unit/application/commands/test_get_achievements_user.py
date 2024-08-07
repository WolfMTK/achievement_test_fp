from typing import Callable, Any

import pytest

from app.application.commands import get_achievements_user
from app.application.dto import GetAchievementUserDTO, Pagination
from app.domain.exceptions import UserNotFoundException


async def test_get_achievements_user(
        achievement_users_gateway: Callable[..., dict[str, Any]]
) -> None:
    gateway = achievement_users_gateway()
    limit = 10
    offset = 0
    data = GetAchievementUserDTO(
        user_id=gateway['user_id'],
        pagination=Pagination(
            limit=limit,
            offset=offset
        )
    )
    data = await get_achievements_user(gateway, data)
    assert data.total == gateway['total']
    assert data.limit == limit
    assert data.offset == offset
    assert data.user_id == gateway['user_id']
    assert len(data.achievements) == gateway['total']


async def test_get_achievements_user_invalid(
        achievement_users_gateway: Callable[..., dict[str, Any]]
) -> None:
    gateway = achievement_users_gateway(is_user_exists=False)
    data = GetAchievementUserDTO(
        user_id=gateway['user_id'],
        pagination=Pagination(
            limit=10,
            offset=0
        )
    )
    with pytest.raises(UserNotFoundException):
        await get_achievements_user(gateway, data)
