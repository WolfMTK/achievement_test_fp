from app.domain.exceptions import UserNotFoundException
from app.domain.models import Users


def check_user(user: Users | None | bool) -> None:
    if not user:
        raise UserNotFoundException()
