from src.presentation.controllers.rma_step_average_controller import RMAStepAverageController
from src.data.rma.rma_use_cases import RMAUseCases
from core.infra.db.repositories.rma_repository import RMARespository
from core.infra.db.repositories.user_repository import UserRepository


def rma_step_average_composer() -> RMAStepAverageController:
    rma_repository = RMARespository()
    user_repository = UserRepository()
    use_case = RMAUseCases(rma_repository, user_repository)
    return RMAStepAverageController(use_case)
