from aioredis import Redis
from src.data.refresh_token_user import RefreshTokenUser
from src.presentation.controllers import RefreshTokenController

from core.infra.db.repositories import UserRepository


def refresh_token_user_composer(redis: Redis) -> RefreshTokenController:
    """Composing refresh_token user route
    :param - None
    :return - object with refresh_token user route
    """

    repository = UserRepository()
    use_case = RefreshTokenUser(repository)
    refresh_token_route = RefreshTokenController(use_case, redis)

    return refresh_token_route
