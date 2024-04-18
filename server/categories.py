from datetime import timedelta

from fastapi import APIRouter, Cookie, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from helper import create_token, hash_password, verify_password
from middleware import (check_category, check_task, decode_refresh_token,
                        get_current_admin_user, get_current_user, get_db)
from models import (CategoryCreate, CategoryUpdateAdmin, TaskCreate,
                    TaskCreateAdmin, TaskUpdate, TaskUpdateAdmin,
                    UserModelLogin, UserModelRegister, UserUpdate)
from schemas import Category, SessionLocal, Task, User
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session, joinedload

categoriesRouter = APIRouter()

@categoriesRouter.post("/")
async def create_category(category_data: CategoryCreate, authUser: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        new_category = Category(
            name = category_data.name,
            user_id=authUser.id
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@categoriesRouter.post("/admin")
async def create_category(category_data: CategoryUpdateAdmin, authUser: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        new_category = Category(
            name = category_data.name,
            user_id=category_data.user_id
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        user = db.query(User).filter(User.id == category_data.user_id).first()
        return {
            "id": new_category.id,
            "name": new_category.name,
            "user_id": new_category.user_id,
            "user":{
                "name": user.name
            }
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@categoriesRouter.patch("/{category_id}")
async def update_category(category_data: CategoryCreate, category: Category = Depends(check_category), authUser: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:

        if category_data.name is not None:
            category.name = category_data.name
       
        db.commit()
        db.refresh(category)
        return category
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@categoriesRouter.patch("/admin/{category_id}")
async def update_category(category_data: CategoryUpdateAdmin, category: Category = Depends(check_category), authUser: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        
        category.name = category_data.name
        category.user_id = category_data.user_id
        
        db.commit()
        db.refresh(category)
        user = db.query(User).filter(User.id == category_data.user_id).first()
        return {
            "id": category.id,
            "name": category.name,
            "user_id": category.user_id,
            "user":{
                "name": user.name
            }
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@categoriesRouter.delete("/{category_id}")
async def delete_category(category: Category = Depends(check_category), db: Session = Depends(get_db)):
    try:
       
        db.delete(category)
        db.commit()
        return {"message": "Category deleted successfully"}
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoriesRouter.get("/")
async def get_category_by_user(authUser: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
       categories = db.query(Category).filter(Category.user_id == authUser.id).all()
       if not categories:
        raise HTTPException(status_code=404, detail="Tasks not found")
       return categories 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@categoriesRouter.get("/admin")
async def get_categories_admin(authUser: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    try:
       categories = db.query(Category).options(joinedload(Category.user)).all()
       if not categories:
        raise HTTPException(status_code=404, detail="Tasks not found")
       return categories 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))