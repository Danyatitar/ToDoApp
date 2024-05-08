import string
from datetime import timedelta

import psycopg2
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from helper import create_token, hash_password, verify_password
from middleware import decode_refresh_token, get_db_connection
from models import UserModelLogin, UserModelRegister
from psycopg2 import sql
from schemas import Category, SessionLocal, Task, User

ACCESS_TOKEN_EXPIRE_MINUTES = 400
REFRESH_TOKEN_EXPIRE_MINUTES = 10080

authRouter = APIRouter()



conn = get_db_connection()

@authRouter.post("/register/")
async def create_user(user: UserModelRegister):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
        existing_user = cursor.fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already registered")


        # hashed_password = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (email, password, name, role) VALUES (%s, %s, %s, %s) RETURNING id",
            (user.email, user.password, user.name, 'user')
        )
        user_id = cursor.fetchone()[0]

        conn.commit()

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
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@authRouter.post("/login/")
async def auth_user(user: UserModelLogin):
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
        existing_user = cursor.fetchone()
        if not existing_user:
            raise HTTPException(status_code=400, detail="User doesn't exist")
        

        if not (user.password == existing_user[3]):  
            raise HTTPException(status_code=400, detail="Incorrect password")
        print(existing_user)
        print(user)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        access_token = create_token(data={"email": existing_user[2], "name": existing_user[1], "role": existing_user[4]}, expires_delta=access_token_expires)
        refresh_token = create_token(data={"email": existing_user[2], "name": existing_user[1], "role": existing_user[4]}, expires_delta=refresh_token_expires)

        user_data = {
            "email": user.email,
            "name": existing_user[1],
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        response = JSONResponse(content=user_data)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite='none')
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@authRouter.post("/logout/")
async def logout():
    data = {"Message": "Logout successful"}
    response = JSONResponse(content=data)
    response.set_cookie(key="refresh_token", value=None, httponly=True, secure=True, samesite='none')
    return response

@authRouter.post("/refresh/")
async def refresh(authUser: User = Depends(decode_refresh_token)):
    access_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(data={"email": authUser.email, "name": authUser.name, "role": authUser.role}, expires_delta=access_token_expires)

    user_data = {
        "email": authUser.email,
        "name": authUser.name,
        "access_token": access_token
    }
    response = JSONResponse(content=user_data)
    return response
