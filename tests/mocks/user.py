import uuid
from typing import Any, Callable, Awaitable

from app.domain.enums import Language
from app.domain.models import Users


def user_gateway_mock(is_user: bool = True) -> dict[str, Any]:
    user_id = uuid.uuid4()
    return {
        'user_id': user_id,
        'get_user': get_user(is_user, user_id)
    }


def get_user(
        is_user: bool,
        user_id: uuid.UUID
) -> Callable[..., Awaitable[Users | None]]:
    async def wrapper(**kwargs: Any) -> Users | None:
        if is_user:
            return Users(
                id=user_id,
                name='test',
                language=Language.RU
            )

    return wrapper
