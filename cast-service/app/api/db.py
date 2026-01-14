import os

from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

DB_POOL_MIN = 1
DB_POOL_MAX = 2

engine = create_engine(DATABASE_URI, pool_size=DB_POOL_MAX, max_overflow=0)
metadata = MetaData()

casts = Table(
    'casts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('nationality', String(20)),
)

database = Database(DATABASE_URI, min_size=DB_POOL_MIN, max_size=DB_POOL_MAX)
