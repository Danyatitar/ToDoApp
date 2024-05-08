from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path
from helper import create_token, hash_password, verify_password
from middleware import get_current_admin_user, get_current_user
from models import (CategoryCreate, CategoryUpdateAdmin, TaskCreate,
                    TaskCreateAdmin, TaskUpdate, TaskUpdateAdmin,
                    UserModelLogin, UserModelRegister, UserUpdate)
from pymongo import MongoClient, ReturnDocument
from schemas import Category, Task, User

client = MongoClient('mongodb+srv://danylo:qwerty123@cluster0.jthorx6.mongodb.net/?authMechanism=DEFAULT')
db = client['todo_app']
tasks_collection = db['tasks']
categories_collection = db['categories']
users_collection = db['users']

tasksRouter = APIRouter()

@tasksRouter.post("/")
async def create_task(task_data:TaskCreate , authUser: User = Depends(get_current_user)):
    try:
        new_task = {
            "title": task_data.title,
            "description": task_data.description,
            "deadline": task_data.deadline,
            "status": task_data.status,
            "user_id": authUser["_id"],  
            "category_id": task_data.category_id
        }
        result = tasks_collection.insert_one(new_task)
        new_task["_id"] = str(result.inserted_id)
        new_task["id"] = str(result.inserted_id)
        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tasksRouter.post("/admin")
async def create_task_admin(task_data:TaskCreateAdmin , authUser: User = Depends(get_current_admin_user)):
    try:
        new_task = {
            "title": task_data.title,
            "description": task_data.description,
            "deadline": task_data.deadline,
            "status": task_data.status,
            "category_id": task_data.category_id,
            "user_id": task_data.user_id
        }
        result = tasks_collection.insert_one(new_task)
        new_task["id"] = str(result.inserted_id)
        new_task["_id"] = str(result.inserted_id)
        category_id = new_task.get("category_id")
        if category_id:
            category = categories_collection.find_one({"_id": ObjectId(category_id)})
            category["_id"] = str(category["_id"])
            category["id"] = str(category["_id"])
            if category:
                new_task["category"] = category
        user_id = new_task.get("user_id")
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        user["_id"] = str(user["_id"])
        user["id"] = str(user["_id"])
        new_task["user"] = user  
        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@tasksRouter.put("/{task_id}")
async def update_task(task_data: TaskUpdate, task_id: str = Path(..., title="The ID of the task to update"), authUser: User = Depends(get_current_user)):
    try:
        updated_task = tasks_collection.find_one_and_update(
            {"_id": ObjectId(task_id)},
            {"$set": {
                "title": task_data.title,
                "description": task_data.description,
                "deadline": task_data.deadline,
                "status": task_data.status.value if task_data.status is not None else None,
                "category_id": task_data.category_id
            }},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        category_id = updated_task.get("category_id")
        if category_id:
            category = categories_collection.find_one({"_id": ObjectId(category_id)})
            category["_id"] = str(category["_id"])
            category["id"] = str(category["_id"])
            if category:
                updated_task["category"] = category
                
        updated_task["_id"] = str(updated_task["_id"])
        updated_task["id"] = str(updated_task["_id"])

        return updated_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tasksRouter.put("/admin/{task_id}")
async def update_task_admin(task_data: TaskUpdateAdmin, task_id: str = Path(..., title="The ID of the task to update"), authUser: User = Depends(get_current_admin_user)):
    try:
        updated_task = tasks_collection.find_one_and_update(
            {"_id": ObjectId(task_id)},
            {"$set": {
                "title": task_data.title,
                "description": task_data.description,
                "deadline": task_data.deadline,
                "status": task_data.status.value if task_data.status is not None else None,
                "category_id": task_data.category_id,
                "user_id": task_data.user_id
            }},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        category_id = updated_task.get("category_id")
        if category_id:
            category = categories_collection.find_one({"_id": ObjectId(category_id)})
            category["_id"] = str(category["_id"])
            category["id"] = str(category["_id"])
            if category:
                updated_task["category"] = category
        user_id = updated_task.get("user_id")
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        user["_id"] = str(user["_id"])
        user["id"] = str(user["_id"])
        updated_task["user"] = user    
        updated_task["_id"] = str(updated_task["_id"])
        updated_task["id"] = str(updated_task["_id"])

        return updated_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tasksRouter.delete("/{task_id}")
async def delete_task(task_id: str = Path(..., title="The ID of the task to delete"), authUser: User = Depends(get_current_user)):
    try:
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@tasksRouter.get("/")
async def get_task_by_user(authUser: User = Depends(get_current_user)):
    try:
        tasks = list(tasks_collection.find({"user_id": authUser["_id"]}))
        if not tasks:
            raise HTTPException(status_code=404, detail="Tasks not found")
        
        for task in tasks:
            category_id = task.get("category_id")
            if category_id:
                category = categories_collection.find_one({"_id": ObjectId(category_id)})
                category["_id"] = str(category["_id"])
                category["id"] = str(category["_id"])
            if category:
                task["category"] = category
            task["_id"] = str(task["_id"])
            task["id"] = str(task["_id"])
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@tasksRouter.get("/admin")
async def get_tasks_admin(authUser: User = Depends(get_current_admin_user)):
    try:
        tasks = list(tasks_collection.find())
        if not tasks:
            raise HTTPException(status_code=404, detail="Tasks not found")
        for task in tasks:
            category_id = task.get("category_id")
            if category_id:
                category = categories_collection.find_one({"_id": ObjectId(category_id)})
                category["_id"] = str(category["_id"])
                category["id"] = str(category["_id"])
            if category:
                task["category"] = category
            user_id = task.get("user_id")
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            user["_id"] = str(user["_id"])
            user["id"] = str(user["_id"])
            task["user"] = user
            task["_id"] = str(task["_id"])
            task["id"] = str(task["_id"])
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
