#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime


class Message:

    def __init__(self, db, **kwargs):
        self.collection = db['messages']

    async def save(self, user, msg, **kw):
        result = await self.collection.insert({'user': user, 'msg': msg, 'time': datetime.now()})
        return result

    async def get_messages(self):
        messages = self.collection.find().sort([('time', 1)])
        result = []
        for message in await messages.to_list(length=None):
            result.append({
                '_id': str(message['_id']),
                'user': message['user'],
                'msg': message['msg'],
                'time': str(message['time']),
            })
        return result
