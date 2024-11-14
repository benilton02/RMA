from src.data.login_user import LoginUser
from src.presentation.controllers import LoginUserController
from core.infra.db.repositories import UserRepository



def login_user_composer(redis) -> LoginUserController:
    """Composing login user route
    :param - None
    :return - object with login user route
    """
    user_repository = UserRepository()
    use_case = LoginUser(user_repository=user_repository)
    login_route = LoginUserController(use_case, redis)

    return login_route
