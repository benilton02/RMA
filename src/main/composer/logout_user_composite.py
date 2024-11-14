from aioredis import Redis
from src.data.logout_user import LogoutUser
from src.presentation.controllers import LogoutUserController


def logout_user_composer(redis: Redis) -> LogoutUserController:
    """Composing logout user route
    :param - None
    :return - object with logout user route
    """

    use_case = LogoutUser()
    logout_route = LogoutUserController(use_case, redis)

    return logout_route
