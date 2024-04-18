from datetime import timedelta

from fastapi import APIRouter, Cookie, Depends, FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from helper import create_token, hash_password, verify_password
from middleware import (check_category, check_task, decode_refresh_token,
                        get_current_admin_user, get_current_user, get_db)
from models import (CategoryCreate, TaskCreate, TaskCreateAdmin, TaskUpdate,
                    TaskUpdateAdmin, UserCreateAdmin, UserModelLogin,
                    UserModelRegister, UserUpdate, UserUpdateAdmin)
from schemas import Category, SessionLocal, Task, User
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session, joinedload

userRouter = APIRouter()


@userRouter.patch("/")
async def update_user(user_data: UserUpdate, authUser: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == authUser.id).first()
        user.name = user_data.name
        db.commit()
        db.refresh(user)
        return user
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@userRouter.patch("/admin/{user_id}")
async def update_user_admin(user_data: UserUpdateAdmin, authUser: User = Depends(get_current_user), user_id: int = Path(..., title="The ID of the task to retrieve"), db: Session = Depends(get_db)):
    try:
        # existing_user = db.query(User).filter(User.email == user_data.email).first()
        # if existing_user:
        #     raise HTTPException(status_code=400, detail="Email is already registered")
        user = db.query(User).filter(User.id == user_id).first()
        user.name = user_data.name
        user.email = user_data.email
        user.role = user_data.role
        db.commit()
        db.refresh(user)
        return user
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@userRouter.post("/admin")
async def create_user(user_data: UserCreateAdmin, authUser: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    try:
        # existing_user = db.query(User).filter(User.email == user_data.email).first()
        # if existing_user:
        #     raise HTTPException(status_code=400, detail="Email is already registered")
        
        hashed_password = hash_password(user_data.password)
        db_user = User(email=user_data.email, password=hashed_password, name=user_data.name, role=user_data.role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@userRouter.get("/")
async def get_user(authUser: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == authUser.id).first()
        return user
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.get("/admin")
async def get_users_admin(authUser: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    try:
       users = db.query(User).all()
       if not users:
        raise HTTPException(status_code=404, detail="Tasks not found")
       return users 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@userRouter.delete("/{user_id}")
async def delete_user(authUser: User = Depends(get_current_admin_user), user_id: int = Path(..., title="The ID of the task to retrieve"), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        db.query(Task).filter(Task.user_id == user_id).delete(synchronize_session=False)
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
