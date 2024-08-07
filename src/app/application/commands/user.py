import logging
from typing import Any

from app.application.dto import UserInfoDTO
from app.domain import services
from app.domain.models import UserId

logger = logging.getLogger(__name__)


async def get_user_info(
        gateway: dict[str, Any],
        data: UserId
) -> UserInfoDTO:
    user = await gateway['get_user'](id=data)
    services.check_user(user)
    logger.debug(f'Get info about the user {user.id}')
    return UserInfoDTO(
        id=user.id,
        name=user.name,
        language=user.language
    )
