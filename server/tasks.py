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

tasksRouter = APIRouter()

@tasksRouter.post("/")
async def create_task(task_data:TaskCreate , authUser: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    try:
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline,
            status=task_data.status,
            user_id= authUser.id,  
            category_id = task_data.category_id
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        new_task_with_category = db.query(Task).filter(Task.id == new_task.id).options(joinedload(Task.category)).first()

        return new_task_with_category
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tasksRouter.post("/admin")
async def create_task_admin(task_data:TaskCreateAdmin , authUser: User = Depends(get_current_admin_user),  db: Session = Depends(get_db)):
    try:
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline,
            status=task_data.status,
            category_id = task_data.category_id,
            user_id = task_data.user_id
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        new_task_with_category = db.query(Task).filter(Task.id == new_task.id).options(joinedload(Task.category)).options(joinedload(Task.user)).first()

        return new_task_with_category
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@tasksRouter.put("/{task_id}")
async def update_task(task_data: TaskUpdate, task: Task = Depends(check_task), authUser: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        print(task_data)
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.deadline is not None:
            task.deadline = task_data.deadline
        if task_data.status is not None:
            task.status = task_data.status.value
        if task_data.category_id is not None:
            category = db.query(Category).filter(Category.id == task_data.category_id, Category.user_id == authUser.id).first()
            if category is None:
                raise HTTPException(status_code=400, detail=str("Category with this id doesn't exists"))
                
        task.category_id = task_data.category_id
        
        db.commit()
        db.refresh(task)
        return task
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        status = 500
        if str(e) == "400: Category with this id doesn't exists":
            status=400
            
        raise HTTPException(status_code=status, detail=str(e))

@tasksRouter.put("/admin/{task_id}")
async def update_task_admin(task_data: TaskUpdateAdmin, task: Task = Depends(check_task), authUser: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == task_data.user_id).first()
        category = db.query(Category).filter(Category.id == task_data.category_id, Category.user_id == task_data.user_id).first()

        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.deadline is not None:
            task.deadline = task_data.deadline
        if task_data.status is not None:
            task.status = task_data.status.value
        if task_data.category_id is not None:
            # category = db.query(Category).filter(Category.id == task_data.category_id, Category.user_id == task_data.user_id).first()
            if category is None:
                raise HTTPException(status_code=400, detail=str("Category with this id doesn't exists"))
            task.category_id = task_data.category_id
        if task_data.user_id is not None:
            # user = db.query(User).filter(User.id == task_data.user_id).first()
            if user is None:
                raise HTTPException(status_code=400, detail=str("User with this id doesn't exists"))         
        task.user_id = task_data.user_id
        
        db.commit()
        db.refresh(task)
        print(user.name)
        if category is None:
            return {
                "deadline": task_data.deadline,
                "description": task_data.description,
                "title": task_data.title,
                "status":task_data.status,
                "id": task.id,
                 "user_id": user.id,
                "user": {
                    "id": user.id,
                    "name": user.name
                }
            }
        else:
            return {
                "deadline": task_data.deadline,
                "description": task_data.description,
                "title": task_data.title,
                "status":task_data.status,
                "id": task.id,
                "user": {
                    "id": user.id,
                    "name": user.name
                },
                "user_id": user.id,
                "category_id": category.id,
                "category": {
                    "id": category.id,
                    "name": category.name
                }
            }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        status = 500
        if str(e) == "400: Category with this id doesn't exists":
            status=400
            
        raise HTTPException(status_code=status, detail=str(e))
    
@tasksRouter.delete("/{task_id}")
async def delete_task(task: Task = Depends(check_task), db: Session = Depends(get_db)):
    try:
        
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@tasksRouter.get("/")
async def get_task_by_user(authUser: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
       tasks = db.query(Task).filter(Task.user_id == authUser.id).options(joinedload(Task.category)).all()
       if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
       return tasks 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@tasksRouter.get("/admin")
async def get_tasks_admin(authUser: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    try:
       tasks = db.query(Task).options(joinedload(Task.category)).options(joinedload(Task.user)).all()
       if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
       return tasks 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))