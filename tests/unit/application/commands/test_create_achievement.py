from typing import Callable, Any

import pytest

from app.application.commands import create_achievement
from app.application.dto import CreateAchievementDTO
from app.domain.exceptions import AchievementExistsException
from tests.mocks.uow import UoWMock


async def test_create_achievement(
        achievement_gateway: Callable[..., dict[str, Any]],
        uow: UoWMock
) -> None:
    gateway = achievement_gateway()
    data = CreateAchievementDTO(
        name='test | тест',
        number_points=10,
        description='test | тест'
    )
    data = await create_achievement(
        gateway, uow, data
    )
    assert data.id == gateway['achievement_id']
    assert uow.commited is True
    assert uow.flushing is False
    assert uow.rolled_back is False


async def test_create_achievement_invalid(
        achievement_gateway: Callable[..., dict[str, Any]],
        uow: UoWMock
) -> None:
    gateway = achievement_gateway(is_check=True)
    data = CreateAchievementDTO(
        name='test | тест',
        number_points=10,
        description='test | тест'
    )
    with pytest.raises(AchievementExistsException):
        await create_achievement(gateway, uow, data)

    assert uow.commited is False
    assert uow.flushing is False
    assert uow.rolled_back is False
