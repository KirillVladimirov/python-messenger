#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from bson.objectid import ObjectId


class User:

    def __init__(self, db, data, id=None):
        self.collection = db['users']
        self.login = data.get('login')
        self.email = data.get('email')
        self.password = data.get('password')
        self.id = id

    async def save(self, user, msg):
        result = await self.collection.insert({'login': user, 'password': msg, 'create_at': datetime.now()})
        self.id = result
        return result

    async def get(self):
        print(1)
        result = await self.collection.find_one({'_id': ObjectId(self.id)})
        self.login = result.get('login')
        self.email = result.get('email')
        self.password = result.get('password')

    async def check(self):
        return await self.collection.find_one({'login': self.login})

    async def save(self):
        user = await self.check()
        if not user:
            result = await self.collection.insert({
                'email': self.email,
                'login': self.login,
                'password': self.password
            })
        else:
            result = 'User exists'
        return result
