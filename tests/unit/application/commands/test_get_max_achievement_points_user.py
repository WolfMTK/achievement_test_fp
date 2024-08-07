from typing import Callable, Any

import pytest

from app.application.commands import (
    get_max_achievement_points_user,
)
from app.domain.exceptions import MaxPointsNotFound


async def test_get_max_achievement_points_user(
        achievement_users_gateway: Callable[..., dict[str, Any]]
) -> None:
    gateway = achievement_users_gateway()
    data = await get_max_achievement_points_user(gateway)
    user_id, name, total = await gateway['get_max_achievement_points_user']()
    assert data.id == user_id
    assert data.name == name
    assert data.total_points == total


async def test_get_max_achievements_points_user_invalid(
        achievement_users_gateway: Callable[..., dict[str, Any]]
) -> None:
    gateway = achievement_users_gateway(is_max_achievement_points=False)
    with pytest.raises(MaxPointsNotFound):
        await get_max_achievement_points_user(gateway)
