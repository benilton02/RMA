from core.infra.db.repositories.rma_repository import RMARespository
from core.infra.db.entities.rma_entity import RMA, UserStatusAssociation
from core.infra.db.repositories.user_repository import UserRepository
from core.utils.permissions import admin_required


class RMAUseCases:
    def __init__(
        self,
        rma_repository: RMARespository,
        user_repository: UserRepository
    ) -> None:
        self.rma_repository = rma_repository
        self.user_repository = user_repository
        
    def create(self, data: dict):
        email = data['logged_user']['email']
        user = self.user_repository.find_user_by_email(email)
        
        if not user:
            return {'success': False, 'code': 400, 'detail': f'The {email} is not registered'}

        rma = data['rma'].__dict__
        current_status = UserStatusAssociation(
            status=data['status'],
            user_id=user.id
        )
        
        rma_entity = RMA(
            product_name=rma['name'],
            defect_description=rma['description'],
            defect=rma['defect'],
            model = rma['model'],
            color = rma['color']
        )
        rma_entity.status.append(current_status)
        result = self.rma_repository.create_rma(rma_entity)

        if result:
            return {
                'success': True,
                'data': {
                        'message': 'RAM created successfully',
                        'rma_id': result
                },
                'code': 200
            }
        
        else:    
            return {'success': False, 'code': 400, 'detail': 'Fail to create RMA!'}

        
    def update(self, data):
        email = data['logged_user']['email']
        user = self.user_repository.find_user_by_email(email)
        
        if not user:
            return {'success': False, 'code': 400, 'detail': f'The {email} is not registered'}
        
        rma_id = data['rma_id']
        rma = self.rma_repository.get_rma_by_id(rma_id)
        if not rma:
            return {'success': False, 'code': 400, 'detail': f'The RMA {rma_id} is not registered'}
        
        value = data['value']
        current_status = UserStatusAssociation(status=value, user_id=user.id)
    
        rma.status.append(current_status)
        result = self.rma_repository.update_rma(rma)
        
        if not result:
            return {'success': False, 'code': 500, 'detail': f'The RMA {rma_id} was not updated'}
        
        return {
                'success': True,
                'data': {
                        'message': 'The RMA was updated successfully',
                },
                'code': 200
            }

        
    def get_rma(self, data):
        rma_id = data['rma_id']
        rma = self.rma_repository.get_rma_by_id(rma_id)
        
        if not rma:
            return {'success': False, 'code': 400, 'detail': f'The RMA {rma_id} is not registered'}
        
        return {
                'success': True,
                'data': {
                        'rma': rma,
                },
                'code': 200
            }


    @admin_required
    def get_common_defect(self, logged_user: dict):
        result = self.rma_repository.get_common_defect()
        return {
            "success": True,
            "data":{
                "items":[
                    {'defect':defect, 'total': total}
                    for defect, total in result
                ]
            }, 
            "code": 200
        }
        
    
    @admin_required
    def step_average(self, logged_user: dict):
        result = self.rma_repository.step_average()

        return {
            "success": True,
            "data": {
                "items":[{
                        "status": status,
                        "avg_duration_hours": round(duration / 3600, 2) if duration else None
                    }
                    for status, duration in result]
            }, 
            "code": 200
        }
                

