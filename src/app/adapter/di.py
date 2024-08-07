import functools
from typing import Any, Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.sqlalchemy_db import (
    create_async_session_maker,
    create_async_session,
)
from app.adapter.sqlalchemy_db.gateways.achievement import (
    create_achievement,
    get_achievements,
    get_total_achievements,
    check_achievement,
)
from app.adapter.sqlalchemy_db.gateways.achievement_user import (
    get_users_with_days_streak,
    get_achievements_user,
    create_achievement_user,
    check_user_id_and_achievement_id,
    check_achievement_user,
    get_max_achievements_user,
    get_total_achievements_user,
    check_user_exists,
    get_max_achievement_points_user,
    get_users_with_max_points_diff,
    get_users_with_min_points_diff,
)
from app.adapter.sqlalchemy_db.gateways.user import get_user
from app.application.protocols.uow import UoW
from app.core import Stub, load_database_config


def new_uow(
        session: AsyncSession = Depends(Stub(AsyncSession))
) -> AsyncSession:
    return session


def get_gateway(
        session: AsyncSession = Depends(Stub(AsyncSession))
) -> dict[str, Any]:
    return {
        'create_achievement': create_achievement(session),
        'get_achievements': get_achievements(session),
        'get_total_achievements': get_total_achievements(session),
        'check_achievement': check_achievement(session),
        'get_achievements_user': get_achievements_user(session),
        'create_achievement_user': create_achievement_user(session),
        'check_user_id_and_achievement_id': check_user_id_and_achievement_id(
            session
        ),
        'check_achievement_user': check_achievement_user(session),
        'get_total_achievements_user': get_total_achievements_user(session),
        'get_max_achievements_user': get_max_achievements_user(session),
        'check_user_exists': check_user_exists(session),
        'get_max_achievement_points_user': get_max_achievement_points_user(
            session
        ),
        'get_users_with_max_points_diff': get_users_with_max_points_diff(
            session
        ),
        'get_users_with_min_points_diff': get_users_with_min_points_diff(
            session
        ),
        'get_users_with_days_streak': get_users_with_days_streak(
            session
        ),
        'get_user': get_user(session)
    }


Gateway = Annotated[dict[str, Any], Depends(get_gateway)]


def init_dependency(app: FastAPI) -> None:
    """ Инициализировать зависимости. """
    db_url = load_database_config().db_url
    session_maker = create_async_session_maker(db_url)

    app.dependency_overrides.update(
        {
            AsyncSession: functools.partial(
                create_async_session,
                session_maker
            ),
            UoW: new_uow,
            Gateway: get_gateway
        }
    )
