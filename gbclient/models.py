import sqlalchemy as sa
from sqlalchemy_aio import ASYNCIO_STRATEGY
import os
from sqlalchemy import (
    Column, Integer, MetaData, Table, Text, create_engine, select)
from sqlalchemy.schema import CreateTable, DropTable
import asyncio


class Db:

    def __init__(self, loop, config_dict):
        self.loop = loop
        sql_path = os.path.join(config_dict['APPLICATION_ROOT'], 'sql', config_dict['CLIENT']['SQLALCHEMY']['DB'])
        sql_uri = 'sqlite:///{}'.format(sql_path)
        self.engine = sa.create_engine(
            sql_uri, strategy=ASYNCIO_STRATEGY
        )

        meta = sa.MetaData()

        self.users = sa.Table(
            'users', meta,
            sa.Column('id', sa.Integer, nullable=False),
            sa.Column('name', sa.String(200), nullable=False),
            sa.Column('email', sa.String(200), nullable=False),
            sa.Column('password', sa.String(200), nullable=False),
            # Indexes #
            sa.PrimaryKeyConstraint('id', name='user_id_pkey'))

        self.messages = sa.Table(
            'messages', meta,
            sa.Column('id', sa.Integer, nullable=False),
            sa.Column('user_id', sa.Integer, nullable=False),
            sa.Column('text', sa.String(200), nullable=False),
            # Indexes #
            sa.PrimaryKeyConstraint('id', name='message_id_pkey'),
            sa.ForeignKeyConstraint(['user_id'], [self.users.c.id],
                                    name='message_user_id_fkey',
                                    ondelete='CASCADE'),
        )

        future = asyncio.Future()
        asyncio.ensure_future(self.get_connection(future))
        self.loop.run_until_complete(future)
        self.conn = future.result()

    async def get_connection(self, future):
        conn = await self.engine.connect()
        future.set_result(conn)

    async def make_tables(self):
        await self.engine.execute(CreateTable(self.users))
        await self.engine.execute(CreateTable(self.messages))

    async def create_user(self, user_name, user_email, user_password):
        await self.conn.execute(self.users.insert().values(
            name=user_name,
            email=user_email,
            password=user_password)
        )

    async def get_user(self, user_name):
        result = await self.conn.execute(self.users.select().where(self.users.c.name == user_name))
        return await result.fetchone()

    async def create_message(self, user, text):
        await self.conn.execute(self.messages.insert().values(
            user_id=user.id,
            text=text)
        )
