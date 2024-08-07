from typing import Callable, Any

import pytest

from app.application.commands import (
    get_users_with_min_points_diff,
)
from app.domain.exceptions import MinPointsDiffNotFoundException


async def test_get_users_with_min_diff(
        achievement_users_gateway: Callable[..., dict[str, Any]]
) -> None:
    gateway = achievement_users_gateway()
    data = await get_users_with_min_points_diff(gateway)
    users = await gateway['get_users_with_min_points_diff']()
    assert len(data) == len(users)

    user_id, name, total, min_diff = users[0]
    data = data[0]
    # минус данной проверки, что данные могут не совпасть
    assert data.id == user_id
    assert data.name == name
    assert data.total_points == total
    assert data.min_diff == min_diff


async def test_get_users_with_min_diff_invalid(
        achievement_users_gateway: Callable[..., dict[str, Any]]
) -> None:
    gateway = achievement_users_gateway(is_user_with_min_points_diff=False)
    with pytest.raises(MinPointsDiffNotFoundException):
        await get_users_with_min_points_diff(gateway)
