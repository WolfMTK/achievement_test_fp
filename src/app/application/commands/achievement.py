import logging
from typing import Any

from app.application.dto import (
    CreateAchievementDTO,
    AchievementResultDTO,
    GetAchievementListDTO, AchievementListDTO,
)
from app.application.protocols import UoW
from app.domain import services

logger = logging.getLogger(__name__)


async def create_achievement(
        gateway: dict[str, Any],
        uow: UoW,
        data: CreateAchievementDTO
) -> AchievementResultDTO:
    services.check_achievement(
        await gateway['check_achievement'](name=data.name)
    )
    achievement = services.create_achievement(**data.model_dump())
    achievement = await gateway['create_achievement_user'](
        id=achievement.id,
        name=achievement.name,
        number_points=achievement.number_points,
        description=achievement.description
    )
    await uow.commit()
    logger.info(
        f'Create new achievement {achievement.id} '
    )
    return AchievementResultDTO(id=achievement.id)


async def get_achievements(
        gateway: dict[str, Any],
        data: GetAchievementListDTO
) -> AchievementListDTO:
    limit = data.pagination.limit
    offset = data.pagination.offset * limit
    achievements = await gateway['get_achievements'](
        limit=limit,
        offset=offset
    )
    total = await gateway['get_total_achievements']()
    achievements = services.get_achievements(achievements)
    logger.debug('Get achievements')
    return AchievementListDTO(
        total=total,
        limit=data.pagination.limit,
        offset=data.pagination.offset,
        achievements=achievements
    )
