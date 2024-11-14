from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.main.configs.db_settings import get_settings


class DBConnectionHandler:
    """Sqlalchemy database connector"""

    def __init__(self) -> None:
        self.__connection_string: str = get_settings().DB_URL
        self.session = None

    def get_engine(self):
        """Return connection engine
        :param - None
        :return - Engine connection to Database
        """
        engine = create_engine(self.__connection_string)

        return engine

    def __enter__(self):
        engine = create_engine(self.__connection_string)
        session_maker = sessionmaker()

        self.session = session_maker(bind=engine)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
