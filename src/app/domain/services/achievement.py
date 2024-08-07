import uuid
from collections.abc import Iterator
from typing import cast

from app.domain.exceptions import AchievementExistsException
from app.domain.models import Achievements, AchievementId


def create_achievement(name: str, number_points: int, description: str):
    achievement_id = cast(AchievementId, uuid.uuid4())
    return Achievements(
        id=achievement_id,
        name=name,
        number_points=number_points,
        description=description
    )


def get_achievements(
        achievements: Iterator[Achievements]
) -> list[Achievements]:
    return [Achievements(
        id=val.id,
        name=val.name,
        number_points=val.number_points,
        description=val.description
    ) for val in achievements]


def check_achievement(value: bool) -> None:
    if value:
        raise AchievementExistsException()
