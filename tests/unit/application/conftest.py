from typing import Callable, Any

import pytest

from tests.mocks.achievement import achievement_gateway_mock
from tests.mocks.achievement_users import achievement_user_gateway_mock
from tests.mocks.uow import UoWMock
from tests.mocks.user import user_gateway_mock


@pytest.fixture()
def achievement_gateway() -> Callable[..., dict[str, Any]]:
    return achievement_gateway_mock


@pytest.fixture()
def achievement_users_gateway() -> Callable[..., dict[str, Any]]:
    return achievement_user_gateway_mock


@pytest.fixture()
def user_gateway() -> Callable[..., dict[str, Any]]:
    return user_gateway_mock


@pytest.fixture()
def uow() -> UoWMock:
    return UoWMock()
