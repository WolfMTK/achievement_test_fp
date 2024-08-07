from typing import Callable, Any

from app.application.commands import (
    get_user_with_days_streak,
)


async def test_get_users_with_days_streak(
        achievement_users_gateway: Callable[..., dict[str, Any]]
) -> None:
    gateway = achievement_users_gateway()
    data = await get_user_with_days_streak(gateway)
    total = len(await gateway['get_users_with_days_streak']())
    assert len(data) == total
