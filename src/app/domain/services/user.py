from app.domain.exceptions import UserNotFoundException
from app.domain.models import Users


def check_user(self, user: Users | None | bool) -> None:
    if not user:
        raise UserNotFoundException()
