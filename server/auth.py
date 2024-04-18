from datetime import timedelta

from fastapi import APIRouter, Cookie, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from helper import create_token, hash_password, verify_password
from middleware import (check_category, check_task, decode_refresh_token,
                        get_current_admin_user, get_current_user, get_db)
from models import (CategoryCreate, TaskCreate, TaskCreateAdmin, TaskUpdate,
                    TaskUpdateAdmin, UserModelLogin, UserModelRegister,
                    UserUpdate)
from schemas import Category, SessionLocal, Task, User
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session, joinedload

ACCESS_TOKEN_EXPIRE_MINUTES = 400
REFRESH_TOKEN_EXPIRE_MINUTES = 10080

authRouter = APIRouter()

@authRouter.post("/register/")
async def create_user(user: UserModelRegister):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already registered")
        
        hashed_password = hash_password(user.password)
        db_user = User(email=user.email, password=hashed_password, name=user.name, role='user')
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        access_token = create_token(data={"email": db_user.email, "name": db_user.name, "role": db_user.role}, expires_delta=access_token_expires)
        refresh_token = create_token(data={"email": db_user.email, "name": db_user.name, "role": db_user.role}, expires_delta=refresh_token_expires)
        user_data = {
            "email": db_user.email,
            "name": db_user.name,
            "access_token": access_token,
            "refresh_token": refresh_token

        }
        response = JSONResponse(content=user_data)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure = True, samesite='none')
        return response
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))
    finally:
        db.close()
        
@authRouter.post("/login/")
async def auth_user(user: UserModelLogin):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if not existing_user:
            raise HTTPException(status_code=400, detail="User doesn't exists")
        
        if not verify_password(user.password, existing_user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")
            
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        access_token = create_token(data={"email": existing_user.email, "name": existing_user.name, "role": existing_user.role}, expires_delta=access_token_expires)
        refresh_token = create_token(data={"email": existing_user.email, "name": existing_user.name, "role": existing_user.role}, expires_delta=refresh_token_expires)

        
        user_data = {
            "email": existing_user.email,
            "name": existing_user.name,
            "access_token": access_token,
            "refresh_token": refresh_token

        }
           
        response = JSONResponse(content=user_data)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure = True, samesite='none')
        return response
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))
    finally:
        db.close()

@authRouter.post("/logout/")
async def logout(authUser: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    data = {
            "Message": "Logout successful",
        }
           
    response = JSONResponse(content=data)
    response.set_cookie(key="refresh_token", value=None, httponly=True, secure = True, samesite='none')
    return response

@authRouter.post("/refresh/")
async def refresh(authUser: User = Depends(decode_refresh_token),  db: Session = Depends(get_db)):
    
    access_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(data={"email": authUser.email, "name": authUser.name, "role": authUser.role}, expires_delta=access_token_expires)
    
        
    user_data = {
            "email": authUser.email,
            "name": authUser.name,
            "access_token": access_token,

        }        
    response = JSONResponse(content=user_data)
    return response
