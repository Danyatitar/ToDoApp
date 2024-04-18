# middleware.py
from typing import Optional, Tuple

from fastapi import Cookie, Depends, Header, HTTPException, Path
from helper import decode_token
from models import TaskUpdate
from schemas import Category, SessionLocal, Task, User
from sqlalchemy.orm import Session, joinedload


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def decode_refresh_token(refresh_token: Optional[str] = Cookie(None,alias="refresh_token"), db: Session = Depends(get_db)):

    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Access denied")
    
    payload = decode_token(refresh_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.email == payload["email"]).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access denied")
    
    access_token = authorization.split("Bearer ")[1]

    payload = decode_token(access_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    user = db.query(User).filter(User.email == payload["email"]).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def get_current_admin_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access denied")
    
    access_token = authorization.split("Bearer ")[1]

    payload = decode_token(access_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    user = db.query(User).filter(User.email == payload["email"], User.role == 'admin').first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def check_task(db: Session = Depends(get_db), task_id: int = Path(..., title="The ID of the task to retrieve"), user: User = Depends(get_current_user)) -> Task:
    task = None
    
    if user.role == 'admin':
        task = db.query(Task).filter(Task.id == task_id).first()    
    else:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).options(joinedload(Task.category)).first()
        
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def check_category(db: Session = Depends(get_db), category_id: int = Path(..., title="The ID of the task to retrieve"), user: User = Depends(get_current_user)) -> Category:
    category = None
    
    if user.role == 'admin':
        category = db.query(Category).filter(Category.id == category_id).first()    
    else:
        category = db.query(Category).filter(Category.id == category_id, Category.user_id == user.id).first()
        
    if category is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return category