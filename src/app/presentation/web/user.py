from fastapi import APIRouter, Depends, HTTPException, status, Path, Query

from app.adapter.di import Gateway
from app.application import commands
from app.application.dto import (
    UserInfoDTO,
    GetAchievementUserDTO,
    Pagination,
    AchievementUserListDTO,
    MaxAchievementsUserResultDTO,
    MaxAchievementPointsUserResultDTO,
    UserWithMaxPointsDiffResultDTO,
    UserWithMinPointsDiffResultDTO
)
from app.domain.exceptions import (
    UserNotFoundException,
    MaxAchievementsNotFound,
    MaxPointsNotFound,
    MaxPointsDiffNotFoundException,
    MinPointsDiffNotFoundException
)
from app.domain.models import UserId
from app.presentation.openapi import (
    EXAMPLE_GET_USER_INFO_RESPONSE,
    EXAMPLE_GET_ACHIEVEMENTS_USER_RESPONSE,
    EXAMPLE_GET_MAX_ACHIEVEMENTS_USER_RESPONSE,
    EXAMPLE_GET_MAX_ACHIEVEMENT_POINTS_USER_RESPONSE,
    EXAMPLE_GET_USERS_WITH_MAX_POINTS_DIFF_RESPONSE,
    EXAMPLE_GET_USERS_WITH_MIN_POINTS_DIFF_RESPONSE,
    EXAMPLE_GET_USERS_WITH_DAYS_STREAK_RESPONSE
)

user_router = APIRouter(prefix='/users')


@user_router.get(
    '/{user_id}/info',
    tags=['Users'],
    name='Получить информацию о пользователе',
    response_model=UserInfoDTO,
    responses=EXAMPLE_GET_USER_INFO_RESPONSE
)
async def get_user_info(
        gateway: Gateway,
        user_id: UserId = Path(
            ...,
            description='Уникальный идентификатор пользователя'
        ),
):
    """
    Информация о пользователе.

    * **user_id** - уникальный идентификатор пользователя (UUID)
    """
    try:
        return await commands.get_user_info(
            gateway,
            user_id
        )
    except UserNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@user_router.get(
    '/{user_id}/achievement',
    name='Получить информацию о выданных пользователю достижениях',
    tags=['Users'],
    response_model=AchievementUserListDTO,
    responses=EXAMPLE_GET_ACHIEVEMENTS_USER_RESPONSE
)
async def get_achievements_user(
        gateway: Gateway,
        limit: int = Query(10, description='Лимит записей'),
        offset: int = Query(0, description='Текущая страница'),
        user_id: UserId = Path(
            ...,
            description='Уникальный идентификатор пользователя'
        ),
):
    """
    Информация о выданных пользователю достижениях
    на выбранном пользователем языке.

    * **user_id** - уникальный идентификатор пользователя

    * **limit** - лимит записей

    * **offset** - текущая страница
    """
    try:
        return await commands.get_achievements_user(
            gateway,
            GetAchievementUserDTO(
                user_id=user_id,
                pagination=Pagination(
                    limit=limit,
                    offset=offset
                )
            )
        )
    except UserNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )


@user_router.get(
    '/top',
    name='Получить пользователя с максимальный количеством достижений',
    tags=['Statistics'],
    response_model=MaxAchievementsUserResultDTO,
    responses=EXAMPLE_GET_MAX_ACHIEVEMENTS_USER_RESPONSE
)
async def get_max_achievements_user(
        gateway: Gateway
):
    """Пользователь с максимальным количеством достижений."""
    try:
        return await commands.get_max_achievements_user(
            gateway
        )
    except MaxAchievementsNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )


@user_router.get(
    '/top-points',
    name='Получить пользователя с максимальным количеством очков достижений',
    tags=['Statistics'],
    response_model=MaxAchievementPointsUserResultDTO,
    responses=EXAMPLE_GET_MAX_ACHIEVEMENT_POINTS_USER_RESPONSE
)
async def get_max_achievement_points_user(
        gateway: Gateway
):
    """Пользователь с максимальным количеством очков достижений."""
    try:
        return await commands.get_max_achievement_points_user(
            gateway
        )
    except MaxPointsNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )


@user_router.get(
    '/max-diff-points',
    name='Получить пользователей с максимальной разностью очков достижений',
    tags=['Statistics'],
    response_model=list[UserWithMaxPointsDiffResultDTO],
    responses=EXAMPLE_GET_USERS_WITH_MAX_POINTS_DIFF_RESPONSE
)
async def get_users_with_max_points_diff(
        gateway: Gateway
):
    """
    Пользователи с максимальной разностью очков достижений.
    """
    try:
        return await commands.get_users_with_max_points_diff(
            gateway
        )
    except MaxPointsDiffNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )


@user_router.get(
    '/min-diff-points',
    name='Получить пользователей с минимальной разностью очков достижений',
    tags=['Statistics'],
    response_model=list[UserWithMinPointsDiffResultDTO],
    responses=EXAMPLE_GET_USERS_WITH_MIN_POINTS_DIFF_RESPONSE
)
async def get_users_with_min_points_diff(
        gateway: Gateway
):
    """
    Пользователи с минимальной разностью очков достижений.
    """
    try:
        return await commands.get_users_with_min_points_diff(
            gateway
        )
    except MinPointsDiffNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )


@user_router.get(
    '/days-streak',
    name='Получить пользователей, которые получали достижения 7 дней подряд',
    tags=['Statistics'],
    response_model=list[UserInfoDTO],
    responses=EXAMPLE_GET_USERS_WITH_DAYS_STREAK_RESPONSE
)
async def get_users_with_days_streak(
        gateway: Gateway
):
    """
    Пользователи, которые получали достижения 7 дней подряд.
    """
    return await commands.get_user_with_days_streak(gateway)
