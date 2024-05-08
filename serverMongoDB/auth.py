from datetime import timedelta

from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse
from helper import create_token, hash_password, verify_password
from middleware import decode_refresh_token, get_current_user
from models import (CategoryCreate, CategoryUpdateAdmin, TaskCreate,
                    TaskCreateAdmin, TaskUpdate, TaskUpdateAdmin,
                    UserModelLogin, UserModelRegister, UserUpdate)
from pymongo import MongoClient
from schemas import Category, Task, User

client = MongoClient('mongodb+srv://danylo:qwerty123@cluster0.jthorx6.mongodb.net/?authMechanism=DEFAULT')
db = client['todo_app']
users_collection = db['users']

ACCESS_TOKEN_EXPIRE_MINUTES = 400
REFRESH_TOKEN_EXPIRE_MINUTES = 10080

authRouter = APIRouter()

@authRouter.post("/register/")
async def create_user(user: UserModelRegister):
    try:
        existing_user = users_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already registered")

        hashed_password = hash_password(user.password)
        db_user = {
            "email": user.email,
            "password": hashed_password,
            "name": user.name,
            "role": 'user'
        }
        result = users_collection.insert_one(db_user)

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        access_token = create_token(data={"email": user.email, "name": user.name, "role": 'user'}, expires_delta=access_token_expires)
        refresh_token = create_token(data={"email": user.email, "name": user.name, "role": 'user'}, expires_delta=refresh_token_expires)

        user_data = {
            "email": user.email,
            "name": user.name,
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        response = JSONResponse(content=user_data)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite='none')
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@authRouter.post("/login/")
async def auth_user(user: UserModelLogin):
    try:
        existing_user = users_collection.find_one({"email": user.email})
        if not existing_user:
            raise HTTPException(status_code=400, detail="User doesn't exist")

        if not verify_password(user.password, existing_user["password"]):
            raise HTTPException(status_code=400, detail="Incorrect password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        access_token = create_token(data={"email": user.email, "name": existing_user["name"], "role": existing_user["role"]}, expires_delta=access_token_expires)
        refresh_token = create_token(data={"email": user.email, "name": existing_user["name"], "role": existing_user["role"]}, expires_delta=refresh_token_expires)

        user_data = {
            "email": user.email,
            "name": existing_user["name"],
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        response = JSONResponse(content=user_data)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite='none')
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@authRouter.post("/logout/")
async def logout(current_user: User = Depends(get_current_user)):
    data = {
        "Message": "Logout successful",
    }
    response = JSONResponse(content=data)
    response.set_cookie(key="refresh_token", value=None, httponly=True, secure=True, samesite='none')
    return response

@authRouter.post("/refresh/")
async def refresh(current_user: User = Depends(decode_refresh_token)):
    access_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(data={"email": current_user["email"], "name": current_user["name"], "role": current_user["role"]}, expires_delta=access_token_expires)

    user_data = {
        "email": current_user["email"],
        "name": current_user["name"],
        "access_token": access_token
    }
    response = JSONResponse(content=user_data)
    return response
