from typing import Optional

from bson.objectid import ObjectId
from fastapi import Cookie, Depends, Header, HTTPException, Path
from helper import decode_token
from pymongo import MongoClient
from schemas import Category, User

client = MongoClient('mongodb+srv://danylo:qwerty123@cluster0.jthorx6.mongodb.net/?authMechanism=DEFAULT')
db = client['todo_app']
users_collection = db['users']
tasks_collection = db['tasks']
categories_collection = db['categories']


def decode_refresh_token(refresh_token: Optional[str] = Cookie(None, alias="refresh_token")):

    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Access denied")
    
    payload = decode_token(refresh_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.users.find_one({"email": payload["email"]})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def get_current_user(authorization: Optional[str] = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access denied")

    access_token = authorization.split("Bearer ")[1]

    payload = decode_token(access_token)
   
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    user = users_collection.find_one({"email": payload["email"]})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return user

def get_current_admin_user(authorization: Optional[str] = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access denied")

    access_token = authorization.split("Bearer ")[1]

    payload = decode_token(access_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    user = users_collection.find_one({"email": payload["email"], "role": "admin"})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["_id"] = str(user["_id"])
    return user

def check_task(task_id: str = Path(..., title="The ID of the task to retrieve"), current_user=Depends(get_current_user)):
    
    task = tasks_collection.find_one({"_id": ObjectId(task_id), "user_id": current_user["_id"]})

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

def check_category(category_id: str = Path(..., title="The ID of the category to retrieve"), current_user=Depends(get_current_user)):
    category = categories_collection.find_one({"_id": ObjectId(category_id), "user_id": current_user["_id"]})

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return category
