
from core.infra.db.config import DBConnectionHandler
from core.infra.db.entities.rma_entity import RMA, UserStatusAssociation, rma_status_association
from sqlalchemy.orm import joinedload, aliased
from sqlalchemy.exc import NoResultFound
from sqlalchemy import func, and_, func, case, cast, Float




class RMARespository:
    
    def create_rma(self, rma: RMA):
        with DBConnectionHandler() as db_connection:
            try:
                db_connection.session.add(rma)
                db_connection.session.flush()
                db_connection.session.commit()
                return rma.id
            
            except:
                db_connection.session.rollback()
                return 0
            

    def update_rma(self, rma_updated: RMA):
        with DBConnectionHandler() as db_connection:
            try:
                db_connection.session.merge(rma_updated)
                db_connection.session.commit()
                return True
            
            except:
                db_connection.session.rollback()
                return False
        
    def get_rma_by_id(self, rma_id: int):
        with DBConnectionHandler() as db_connection:
            try:
                data = (
                    db_connection.session.query(RMA)
                    .options(
                    joinedload(RMA.status).joinedload(UserStatusAssociation.user).load_only("email", "full_name")
                )
                    .filter_by(id=rma_id)
                    .one()
                )

                return data
            except NoResultFound:
                return []
            
    
    def get_common_defect(self):
        with DBConnectionHandler() as db_connection:
            try:
                common_defects = (
                    db_connection.session.query(
                        RMA.defect, func.count(RMA.defect).label('defect_count')
                    )
                    .group_by(RMA.defect)
                    .order_by(func.count(RMA.defect).desc())
                    .all()
                )
                return common_defects

            except Exception as e:
                return []


    def step_average(self):
        with DBConnectionHandler() as db_connection:
            current_status = aliased(UserStatusAssociation)
            next_status = aliased(UserStatusAssociation)

            query = (
                db_connection.session.query(
                    current_status.status.label('step'),
                    func.avg(
                        cast(
                            (func.extract('epoch', next_status.created_at) - func.extract('epoch', current_status.created_at)),
                            Float
                        )
                    ).label('average_duration_seconds')
                )
                .join(
                    rma_status_association, rma_status_association.c.user_status_association_id == current_status.id
                )
                .join(
                    next_status,
                    (rma_status_association.c.rma_id == rma_status_association.c.rma_id) & 
                    (next_status.created_at > current_status.created_at)
                )
                .group_by(current_status.status)
                .order_by(current_status.status)
            )

            return query.all()