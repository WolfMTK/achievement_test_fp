from fastapi import APIRouter, Depends, HTTPException, status, Body, Query

from app.adapter.di import Gateway
from app.application import commands
from app.application.dto import (
    CreateAchievementDTO,
    AchievementResultDTO,
    Pagination,
    GetAchievementListDTO,
    AchievementListDTO,
    NewAchievementUserDTO,
    AchievementUserResultDTO,
)
from app.application.protocols.uow import UoW
from app.domain.exceptions import (
    AchievementExistsException,
    AchievementUserNotFoundException,
    AchievementUserExistsException
)
from app.presentation.openapi import (
    EXAMPLE_CREATE_ACHIEVEMENT_BODY,
    EXAMPLE_CREATE_ACHIEVEMENT_RESPONSE,
    EXAMPLE_GET_ACHIEVEMENTS_RESPONSE,
    EXAMPLE_ADD_ACHIEVEMENT_USER_BODY,
    EXAMPLE_ADD_ACHIEVEMENT_USER_RESPONSE,
)

achievement_router = APIRouter(prefix='/achievement', tags=['Achievement'])


@achievement_router.post(
    '/',
    name='Добавить достижения',
    response_model=AchievementResultDTO,
    status_code=status.HTTP_201_CREATED,
    responses=EXAMPLE_CREATE_ACHIEVEMENT_RESPONSE
)
async def create_achievement(
        gateway: Gateway,
        uow: UoW = Depends(),
        achievement: CreateAchievementDTO = Body(
            ...,
            example=EXAMPLE_CREATE_ACHIEVEMENT_BODY),
):
    """
    Добавление достижений.

    * **name** - название достижения (указывать RU|EN версии)

    * **numberPoints** - количество очков

    * **description** - описание достижения (указывать RU|EN версии)
    """
    try:
        return await commands.create_achievement(
            gateway,
            uow,
            achievement
        )
    except AchievementExistsException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@achievement_router.get(
    '/',
    name='Получить информацию о всех доступных достижениях',
    response_model=AchievementListDTO,
    responses=EXAMPLE_GET_ACHIEVEMENTS_RESPONSE
)
async def get_achievements(
        gateway: Gateway,
        limit: int = Query(10, description='Лимит записей'),
        offset: int = Query(0, description='Текущая страница'),
):
    """
    Информация о всех доступных достижениях.

    * **limit** - лимит записей

    * **offset** - текущая страница
    """
    return await commands.get_achievements(
        gateway,
        GetAchievementListDTO(Pagination(limit=limit, offset=offset))
    )


@achievement_router.post(
    '/users',
    name='Выдать достижение пользователю.',
    response_model=AchievementUserResultDTO,
    status_code=status.HTTP_201_CREATED,
    responses=EXAMPLE_ADD_ACHIEVEMENT_USER_RESPONSE
)
async def add_achievement_user(
        gateway: Gateway,
        uow: UoW = Depends(),
        achievement_user: NewAchievementUserDTO = Body(
            ...,
            example=EXAMPLE_ADD_ACHIEVEMENT_USER_BODY
        ),
):
    """
    Выдает достижение пользователю с сохранением времени выдачи.

    * **userId** - уникальный идентификатор пользователя

    * **achievementId** - уникальный идентификатор достижения
    """
    try:
        return await commands.add_achievement_user(
            gateway,
            uow,
            achievement_user
        )
    except AchievementUserExistsException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    except AchievementUserNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
