import urllib.parse

from sqlalchemy import create_engine
import sqlalchemy

DB_NAME = 'postgres'
password = urllib.parse.quote_plus('postgres')
user = 'postgres'
print('password', password)
print('user', user)

DB_URL = f'postgresql+pg8000://{user}:{password}@localhost'

engine = create_engine(DB_URL, isolation_level='AUTOCOMMIT')

conn = engine.connect()

conn.execute(f'CREATE DATABASE {DB_NAME}')
