import datetime as dt
from collections.abc import Iterator

from app.core.constants import LANGUAGE
from app.domain.exceptions import (
    AchievementUserExistsException,
    AchievementUserNotFoundException,
    MaxAchievementsNotFound,
    MaxPointsNotFound,
    MaxPointsDiffNotFoundException,
    MinPointsDiffNotFoundException,
)
from app.domain.models import UsersAchievements, Achievements, UserId


def check_max_points_diff_users(
        values: Iterator[tuple[UserId, str, int, int]] | None
) -> None:
    if values is None:
        raise MaxPointsDiffNotFoundException()


def check_min_points_diff_users(
        values: Iterator[tuple[UserId, str, int, int]] | None
) -> None:
    if values is None:
        raise MinPointsDiffNotFoundException()


def check_max_points_user(
        value: tuple[UserId, str, int] | None
) -> None:
    if value is None:
        raise MaxPointsNotFound()


def check_max_achievements_user(
        value: tuple[UserId, str, int] | None
) -> None:
    if value is None:
        raise MaxAchievementsNotFound()


def check_achievement_and_user(value: bool) -> None:
    if not value:
        raise AchievementUserNotFoundException()


def check_achievement_user(value: bool) -> None:
    if value:
        raise AchievementUserExistsException()


def get_date_on(date_on: dt.datetime) -> str:
    return date_on.strftime('%Y-%m-%d %H:%M')


def get_achievement(
        data: Iterator[UsersAchievements]
) -> list[Achievements]:
    result = []
    for val in data:
        achievement = val.achievement
        language = val.user.language
        name = achievement.name.split('|')[LANGUAGE[language.lower()]]
        description = (
            achievement
            .description.split('|')[LANGUAGE[language.lower()]]
        )
        result.append(
            Achievements(
                id=achievement.id,
                name=name,
                number_points=achievement.number_points,
                description=description
            )
        )
    return result
