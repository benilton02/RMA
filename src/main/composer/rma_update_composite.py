from src.presentation.controllers.rma_update_controller import RMAUpdatController
from src.data.rma.rma_use_cases import RMAUseCases
from core.infra.db.repositories.rma_repository import RMARespository
from core.infra.db.repositories.user_repository import UserRepository


def rma_update_composer() -> RMAUpdatController:
    rma_repository = RMARespository()
    user_repository = UserRepository()
    use_case = RMAUseCases(rma_repository, user_repository)
    return RMAUpdatController(use_case)
