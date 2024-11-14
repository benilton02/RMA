# pylint: disable=E1101
from datetime import datetime, timedelta
from dateutil import tz

from sqlalchemy import String, text, func, select
from sqlalchemy.sql import func as f
from typing import List
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload, immediateload
from sqlalchemy.sql.expression import cast

from sqlalchemy.sql import func
from core.domain.models import Role, User as UsersModel
from core.domain.repositories import UserRepositoryInterface
from core.infra.db.config import DBConnectionHandler
from core.infra.db.entities import Users
from core.infra.db.entities import Roles as RolesEntity
from core.infra.db.entities.user_entity import (
    user_roles_table as UsersRolesTable,
)
from sqlalchemy import or_, and_

from .role_repository import RoleRepository

class UserRepository(UserRepositoryInterface):
    """Users repository"""

    @classmethod
    def insert_user(cls, user: UsersModel) -> Users:
        """Insert one user
        :param - user: UsersModel
        :return - tuple with user inserted
        """

        with DBConnectionHandler() as db_connection:
            try:
                list_roles = []
                for role in user.roles:
                    if role.id == 0:
                        raise Exception(
                            'Exists roles not registered in this user'
                        )
                    list_roles.append(RoleRepository.find_Role(role)[0])

                new_user = Users(user)
                new_user.roles = list_roles
                db_connection.session.add(new_user)
                db_connection.session.commit()

                user.id = new_user.id
                return user
            except Exception as e:
                print(e)
                db_connection.session.rollback()
                raise e
            finally:
                db_connection.session.close()

        return None

    @classmethod
    def update_user(cls, user: UsersModel) -> Users:
        """Update one user
        :param - user: UsersModel
        :return - tuple with user inserted
        """

        with DBConnectionHandler() as db_connection:
            try:
                user_db = UserRepository.find_user({'id': user.id})

                if len(user_db) == 0:
                    raise Exception('User not found')
                user_db = user_db[0]

                list_roles = []
                for role in user.roles:
                    if role.id == 0:
                        raise Exception(
                            'Exists roles not registered in this user'
                        )
                    list_roles.append(RoleRepository.find_Role(role)[0])

                user_db.full_name = user.full_name
                user_db.email = user.email
                user_db.password = user.password
                user_db.roles = list_roles
                user_db.blocked = user.blocked

                db_connection.session.merge(user_db)
                db_connection.session.commit()

                return UserRepository.find_user({'id': user.id})[0]
            except Exception as e:
                print(e)
                db_connection.session.rollback()
                raise e
            finally:
                db_connection.session.close()

        return None

    @classmethod
    def find_user(cls, user: dict) -> List[Users]:
        """Select users
        :return - List of users
        """
        with DBConnectionHandler() as db_connection:
            try:
                query_data = None

                if 'id' in user:
                    data = (
                        db_connection.session.query(Users)
                        .options(joinedload(Users.roles))
                        .filter_by(id=user['id'])
                        .one()
                    )
                    query_data = [data]
                elif 'full_name' in user:
                    data = (
                        db_connection.session.query(Users)
                        .options(joinedload(Users.roles))
                        .filter_by(full_name=user['full_name'])
                        .one()
                    )
                    query_data = [data]
                elif 'email' in user:

                    data = (
                        db_connection.session.query(Users)
                        .options(joinedload(Users.roles))
                        .filter_by(email=user['email'])
                        .one()
                    )
                    query_data = [data]

                return query_data
            except NoResultFound:
                return []
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

    def find_user_by_email(cls, user_email):
        with DBConnectionHandler() as db_connection:
            try:
                data = (
                    db_connection.session.query(Users)
                    .filter_by(email=user_email)
                    .one()
                )

                return data
            except NoResultFound:
                return []
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()


    @classmethod
    def count_all_users_not_admin_where_roles_value_startswith(
        cls, value: str
    ) -> int:
        with DBConnectionHandler() as db_connection:
            try:
                return (
                    db_connection.session.query(Users)
                    .filter(
                        and_(
                            ~Users.roles.any(RolesEntity.value == 'ADMIN'),
                            Users.roles.any(
                                RolesEntity.value.startswith(value)
                            ),
                        )
                    )
                    .count()
                )

            except Exception:
                return 1


    @classmethod
    def all_users_where_roles_value_startswith(cls, value: str):
        with DBConnectionHandler() as db_connection:
            return (
                db_connection.session.query(Users)
                .options(joinedload(Users.roles))
                .filter(
                    and_(
                        Users.roles.any(RolesEntity.value.startswith(value)),
                    )
                )
                .all()
            )


    @classmethod
    def full_text_search(
        cls,
        text: str,
        branch_value: str,
        today: bool = False,
    ):
        with DBConnectionHandler() as db_connection:
            queryset = (
                db_connection.session.query(Users)
                .options(joinedload(Users.tracking_data))
                .filter(
                    Users.roles.any(
                        RolesEntity.value.startswith(branch_value)
                    ),
                )
                .where(
                    Users.full_name.like(f'%{text}%')
                    | Users.email.like(f'%{text}%')
                    | cast(Users.id, String).like(f'%{text}%')
                )
            )

    #         return queryset.all()





 

    

    


                