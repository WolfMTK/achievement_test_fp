import logging
from typing import Any

from app.application.dto import (
    GetAchievementUserDTO,
    AchievementUserListDTO,
    MaxAchievementPointsUserResultDTO,
    MaxAchievementsUserResultDTO,
    AchievementUserResultDTO,
    NewAchievementUserDTO,
    UserInfoDTO,
    UserWithMaxPointsDiffResultDTO, UserWithMinPointsDiffResultDTO,
)
from app.application.protocols.uow import UoW
from app.domain import services

logger = logging.getLogger(__name__)


async def get_achievements_user(
        gateway: dict[str, Any],
        data: GetAchievementUserDTO
) -> AchievementUserListDTO:
    services.check_user(
        await gateway['check_user_exists'](data.user_id)
    )
    limit = data.pagination.limit
    offset = data.pagination.offset * limit
    achievement_user = await gateway['get_achievements_user'](
        user_id=data.user_id,
        limit=limit,
        offset=offset
    )
    total = await gateway['get_total_achievements_user'](user_id=data.user_id)
    logger.debug(f'Get achievements the user {data.user_id}')
    return AchievementUserListDTO(
        total=total,
        limit=data.pagination.limit,
        offset=data.pagination.offset,
        user_id=data.user_id,
        achievements=services.get_achievement(achievement_user)
    )


async def get_max_achievement_points_user(
        gateway: dict[str, Any],
) -> MaxAchievementPointsUserResultDTO:
    data = await gateway['get_max_achievement_points_user']()
    services.check_max_points_user(data)
    user_id, name, total = data
    logger.debug('Get max achievement points the user')
    return MaxAchievementPointsUserResultDTO(
        id=user_id,
        name=name,
        total_points=total
    )


async def get_max_achievements_user(
        gateway: dict[str, Any]
) -> MaxAchievementsUserResultDTO:
    data = await gateway['get_max_achievements_user']()
    services.check_max_achievements_user(data)
    user_id, name, count = data
    logging.debug('Get max achievements the user')
    return MaxAchievementsUserResultDTO(
        id=user_id,
        name=name,
        count=count
    )


async def add_achievement_user(
        gateway: dict[str, Any],
        uow: UoW,
        data: NewAchievementUserDTO
) -> AchievementUserResultDTO:
    services.check_achievement_and_user(
        await gateway['check_user_id_and_achievement_id'](
            **data.model_dump()
        )
    )
    services.check_achievement_user(
        await gateway['check_achievement_user'](**data.model_dump())
    )
    achievement_user = await gateway['create_achievement_user'](
        **data.model_dump()
    )
    await uow.commit()
    logger.info(
        f'Add new achievement {achievement_user.achievement_id} '
        f'the user {achievement_user.user_id}'
    )
    return AchievementUserResultDTO(
        user_id=achievement_user.user_id,
        achievement_id=achievement_user.achievement_id,
        date_on=services.get_date_on(achievement_user.date_on)
    )


async def get_user_with_days_streak(
        gateway: dict[str, Any]
) -> list[UserInfoDTO]:
    users = await gateway['get_users_with_days_streak']()
    logging.debug('Get users with days streak')
    return [UserInfoDTO(
        id=user.id,
        name=user.name,
        language=user.language
    ) for user in users]


async def get_users_with_max_points_diff(
        gateway: dict[str, Any]
) -> list[UserWithMaxPointsDiffResultDTO]:
    data = await gateway['get_users_with_max_points_diff']()
    services.check_max_points_diff_users(data)
    logger.debug('Get users with max points diff')
    return [UserWithMaxPointsDiffResultDTO(
        id=user_id,
        name=name,
        total_points=total,
        max_diff=max_diff
    ) for user_id, name, total, max_diff in data]


async def get_users_with_min_points_diff(
        gateway: dict[str, Any]
) -> list[UserWithMinPointsDiffResultDTO]:
    data = await gateway['get_users_with_min_points_diff']()
    services.check_min_points_diff_users(data)
    logger.debug('Get users with min points diff')
    return [UserWithMinPointsDiffResultDTO(
        id=user_id,
        name=name,
        total_points=total,
        min_diff=min_diff
    ) for user_id, name, total, min_diff in data]
