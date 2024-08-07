from typing import Callable, Any

import pytest

from app.application.commands import get_user_info
from app.domain.exceptions import UserNotFoundException


async def test_get_user_info(
        user_gateway: Callable[..., dict[str, Any]]
) -> None:
    gateway = user_gateway()
    user = await gateway['get_user']()
    data = await get_user_info(gateway, user.id)
    assert data.id == user.id
    assert data.name == user.name
    assert data.language == user.language


async def test_get_user_info_invalid(
        user_gateway: Callable[..., dict[str, Any]]
) -> None:
    gateway = user_gateway(is_user=False)
    with pytest.raises(UserNotFoundException):
        await get_user_info(gateway, gateway['user_id'])
