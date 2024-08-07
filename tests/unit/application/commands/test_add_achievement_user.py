from typing import Callable, Any

import pytest

from app.application.commands import add_achievement_user
from app.application.dto import NewAchievementUserDTO
from app.domain.exceptions import (
    AchievementUserNotFoundException,
    AchievementUserExistsException,
)
from tests.mocks.uow import UoWMock


async def test_add_achievement_user(
        achievement_users_gateway: Callable[..., dict[str, Any]],
        uow: UoWMock
) -> None:
    gateway = achievement_users_gateway()
    data = NewAchievementUserDTO(
        user_id=gateway['user_id'],
        achievement_id=gateway['achievement_id']
    )
    data = await add_achievement_user(
        gateway, uow, data
    )
    assert data.user_id == gateway['user_id']
    assert data.achievement_id == gateway['achievement_id']
    assert data.date_on == gateway['date_on'].strftime('%Y-%m-%d %H:%M')

    assert uow.commited is True
    assert uow.flushing is False
    assert uow.rolled_back is False


async def test_add_achievement_user_invalid_id(
        achievement_users_gateway: Callable[..., dict[str, Any]],
        uow: UoWMock
) -> None:
    gateway = achievement_users_gateway(is_user_id_and_achievement_id=False)
    data = NewAchievementUserDTO(
        user_id=gateway['user_id'],
        achievement_id=gateway['achievement_id']
    )
    with pytest.raises(AchievementUserNotFoundException):
        await add_achievement_user(gateway, uow, data)

    assert uow.commited is False
    assert uow.flushing is False
    assert uow.rolled_back is False


async def test_add_achievement_user_invalid(
        achievement_users_gateway: Callable[..., dict[str, Any]],
        uow: UoWMock
) -> None:
    gateway = achievement_users_gateway(is_achievement_user=True)
    data = NewAchievementUserDTO(
        user_id=gateway['user_id'],
        achievement_id=gateway['achievement_id']
    )
    with pytest.raises(AchievementUserExistsException):
        await add_achievement_user(gateway, uow, data)

    assert uow.commited is False
    assert uow.flushing is False
    assert uow.rolled_back is False
