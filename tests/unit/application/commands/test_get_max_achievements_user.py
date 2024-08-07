from typing import Callable, Any

import pytest

from app.application.commands import (
    get_max_achievements_user,
)
from app.domain.exceptions import MaxAchievementsNotFound


async def test_get_max_achievements_user(
        achievement_users_gateway: Callable[..., dict[str, Any]]
) -> None:
    gateway = achievement_users_gateway()
    data = await get_max_achievements_user(gateway)
    user_id, name, total = await gateway['get_max_achievements_user']()
    assert data.id == user_id
    assert data.name == name
    assert data.count == total


async def test_get_max_achievements_user_invalid(
        achievement_users_gateway: Callable[..., dict[str, Any]]
) -> None:
    gateway = achievement_users_gateway(is_max_achievements_user=False)
    with pytest.raises(MaxAchievementsNotFound):
        await get_max_achievements_user(gateway)
