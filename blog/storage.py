import contextlib
import os

import sqlalchemy
from sqlalchemy import sql

metadata = sqlalchemy.MetaData()

create_all = metadata.create_all

posts = sqlalchemy.Table('posts', metadata,
            sqlalchemy.Column('content', sqlalchemy.String),
)

def get_engine():
    return sqlalchemy.create_engine(os.environ['BLOG_DATABASE'])

def add_post(engine, content):
    with contextlib.closing(engine.connect()) as conn:
        conn.execute(posts.insert().values(content=content))

def get_posts(engine):
    with contextlib.closing(engine.connect()) as conn:
        return list(conn.execute(sql.select([posts])))
