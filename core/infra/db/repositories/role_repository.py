# pylint: disable=E1101

from sqlalchemy.exc import NoResultFound

from core.domain.models import Role as RoleModel
from core.domain.repositories import RoleRepositoryInterface
from core.infra.db.config import DBConnectionHandler
from core.infra.db.entities import Roles as RolesEntity


class RoleRepository(RoleRepositoryInterface):
    """RoleModel repository"""

    @classmethod
    def insert_role(cls, role: RoleModel):
        """Insert one role
        :param - role: RoleModel
        :return - tuple with role inserted
        """

        with DBConnectionHandler() as db_connection:
            try:
                new_role = RolesEntity(role)
                db_connection.session.add(new_role)
                db_connection.session.commit()

                role.id = new_role.id
                return role
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return None

    @classmethod
    def delete_role(cls, role_id: int):
        """Delete one role
        :param - role_id: int
        :return - tuple with role inserted
        """

        with DBConnectionHandler() as db_connection:
            try:
                deleted_role = (
                    db_connection.session.query(RolesEntity)
                    .filter(RolesEntity.id == role_id)
                    .first()
                )

                db_connection.session.delete(deleted_role)
                db_connection.session.commit()

                return deleted_role
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return None

    @classmethod
    def list_role(cls) -> list[RoleModel]:
        """Lind RoleModel"""
        with DBConnectionHandler() as db_connection:
            try:
                data = db_connection.session.query(RolesEntity).all()
                return data
            except NoResultFound:
                return []
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return None

    @classmethod
    def find_Role(cls, role: RoleModel) -> list[RoleModel]:
        """Select roles
        :return - List of roles
        """
        with DBConnectionHandler() as db_connection:
            try:
                query_data = None

                if role.id != 0:
                    data = (
                        db_connection.session.query(RolesEntity)
                        .filter_by(id=role.id)
                        .all()
                    )
                    query_data = data
                elif len(role.value.strip()) > 0:

                    data = (
                        db_connection.session.query(RolesEntity)
                        .filter_by(value=role.value)
                        .all()
                    )
                    query_data = data
                elif len(role.label.strip()) > 0:

                    data = (
                        db_connection.session.query(RolesEntity)
                        .filter_by(label=role.label)
                        .all()
                    )
                    query_data = data

                return query_data
            except NoResultFound:
                return []
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return None
