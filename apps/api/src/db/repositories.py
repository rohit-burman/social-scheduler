from typing import Any,Optional
from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

class UserRepository:
    def __init__(self,db:AsyncDatabase)->None:
        self.collection = db["users"]


    async def create(self,document:dict[str,Any])->dict[str,Any]:
        res=await self.collection.insert_one(document)
        document["_id"]=res.inserted_id
        return document

    async def get_by_email(self,email:str)->dict[str,Any]|None:
        return await self.collection.find_one({'email':email})


    async def get_by_id(self,user_id:str)->dict[str,Any]|None:
        if not ObjectId.is_valid(user_id): return None
        return await self.collection.find_one({'_id':ObjectId(user_id)})

    


