from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse
from helper import hash_password, verify_password
from middleware import get_current_admin_user, get_current_user
from models import (CategoryCreate, CategoryUpdateAdmin, TaskCreate,
                    TaskCreateAdmin, TaskUpdate, TaskUpdateAdmin,
                    UserCreateAdmin, UserModelLogin, UserModelRegister,
                    UserUpdate, UserUpdateAdmin)
from pymongo import MongoClient, ReturnDocument
from schemas import Category, Task, User

client = MongoClient('mongodb+srv://danylo:qwerty123@cluster0.jthorx6.mongodb.net/?authMechanism=DEFAULT')
db = client['todo_app']
users_collection = db['users']

userRouter = APIRouter()

@userRouter.patch("/")
async def update_user(user_data: UserUpdate, authUser: User = Depends(get_current_user)):
    try:
        user = users_collection.find_one_and_update(
            {"_id": ObjectId(authUser["_id"])},
            {"$set": {"name": user_data.name}},
            return_document=ReturnDocument.AFTER
        )
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user["_id"] = str(user["_id"])
        user["id"] = str(user["_id"])
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.patch("/admin/{user_id}")
async def update_user_admin(user_data: UserUpdateAdmin, user_id: str = Path(..., title="The ID of the user to update"), authUser: User = Depends(get_current_user)):
    try:
        user = users_collection.find_one_and_update(
            {"_id": ObjectId(authUser["_id"])},
            {"_id": ObjectId(user_id)}, {"$set": {"name": user_data.name, "email": user_data.email, "role": user_data.role}},
            return_document=ReturnDocument.AFTER
        )
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user["_id"] = str(user["_id"])
        user["id"] = str(user["_id"])
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.post("/admin")
async def create_user(user_data: UserCreateAdmin, authUser: User = Depends(get_current_admin_user)):
    try:

        hashed_password = hash_password(user_data.password)
        db_user = {
            "email": user_data.email,
            "password": hashed_password,
            "name": user_data.name,
            "role": user_data.role
        }
        result = users_collection.insert_one(db_user)
        db_user["id"] = str(result.inserted_id)
        db_user["_id"] = str(result.inserted_id)
        print(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.get("/")
async def get_user(authUser: User = Depends(get_current_user)):
    try:
        authUser["id"] = str(authUser["_id"])
        return authUser
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.get("/admin")
async def get_users_admin(authUser: User = Depends(get_current_admin_user)):
    try:
        users = list(users_collection.find())
        if not users:
            raise HTTPException(status_code=404, detail="Users not found")
        for user in users:
            user["_id"] = str(user["_id"])
            user["id"] = str(user["_id"])
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.delete("/{user_id}")
async def delete_user(user_id: str = Path(..., title="The ID of the user to delete"), authUser: User = Depends(get_current_admin_user)):
    try:
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
