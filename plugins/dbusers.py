import time
import datetime
import motor.motor_asyncio
from config import DB_NAME, DB_URI

DATABASE_NAME = DB_NAME
DATABASE_URI = DB_URI


class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.users = self.db.uersz
        self.grp = self.db.groups


    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )

    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )

    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)


    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    
    async def get_all_users(self):
        return self.col.find({})

    async def get_user(self, user_id):
        user_data = await self.users.find_one({"id": user_id})
        return user_data
            
    async def update_user(self, user_data):
        await self.users.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def has_premium_access(self, user_id):
        user_data = await self.get_user(user_id)
        if user_data:
            expiry_time = user_data.get("expiry_time")
            if expiry_time is None:
                # User previously used the free trial, but it has ended.
                return False
            elif isinstance(expiry_time, datetime.datetime) and datetime.datetime.now() <= expiry_time:
                return True
            else:
                await self.users.update_one({"id": user_id}, {"$set": {"expiry_time": None}})
        return False
    
    async def check_remaining_uasge(self, userid):
        user_id = userid
        user_data = await self.get_user(user_id)        
        expiry_time = user_data.get("expiry_time")
        # Calculate remaining time
        remaining_time = expiry_time - datetime.datetime.now()
        return remaining_time

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})


db = Database(DATABASE_URI, DATABASE_NAME)
