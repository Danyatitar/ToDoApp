from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from helper import create_token, hash_password, verify_password
from middleware import get_current_admin_user, get_current_user
from models import (CategoryCreate, CategoryUpdateAdmin, TaskCreate,
                    TaskCreateAdmin, TaskUpdate, TaskUpdateAdmin,
                    UserModelLogin, UserModelRegister, UserUpdate)
from pymongo import MongoClient, ReturnDocument
from schemas import Category, Task, User

client = MongoClient('mongodb+srv://danylo:qwerty123@cluster0.jthorx6.mongodb.net/?authMechanism=DEFAULT')
db = client['todo_app']
categories_collection = db['categories']
users_collection = db['users']

categoriesRouter = APIRouter()

@categoriesRouter.post("/")
async def create_category(category_data: CategoryCreate, authUser: User = Depends(get_current_user)):
    try:
        new_category = categories_collection.insert_one({
            "name": category_data.name,
            "user_id": authUser["_id"]
        })
        new_category_id = str(new_category.inserted_id)
        return {"id": new_category_id, "name": category_data.name, "user_id": authUser["_id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@categoriesRouter.post("/admin")
async def create_category(category_data: CategoryUpdateAdmin, authUser: User = Depends(get_current_user)):
    try:
        new_category = {
            "name": category_data.name,
            "user_id": category_data.user_id
        }
        result = categories_collection.insert_one(new_category)
        new_category_id = str(result.inserted_id)
        user = users_collection.find_one({"_id": ObjectId(category_data.user_id)})
        return {
            "id": new_category_id,
            "name": new_category["name"],
            "user_id": new_category["user_id"],
            "user": {
                "name": user["name"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@categoriesRouter.patch("/{category_id}")
async def update_category(category_data: CategoryCreate, category_id: str, authUser: User = Depends(get_current_user)):
    try:
        
        update_fields = {}
        if category_data.name is not None:
            update_fields["name"] = category_data.name
            
        updated_category = categories_collection.find_one_and_update(
            {"_id": ObjectId(category_id)},
            {"$set": update_fields},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated_category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        updated_category["_id"] = str(updated_category["_id"])
        updated_category["id"] = str(updated_category["_id"])
        
        return updated_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@categoriesRouter.patch("/admin/{category_id}")
async def update_category(category_data: CategoryUpdateAdmin, category_id: str, authUser: User = Depends(get_current_user)):
    try:
        category = categories_collection.find_one({"_id": ObjectId(category_id)})
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        update_fields = {}
        if category_data.name is not None:
            update_fields["name"] = category_data.name
        if category_data.user_id is not None:
            update_fields["user_id"] = category_data.user_id
        
        updated_category = categories_collection.find_one_and_update(
            {"_id": ObjectId(category_id)},
            {"$set": update_fields},
            return_document=ReturnDocument.AFTER
        )
        
        if updated_category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        
        user_id = updated_category["user_id"]
        if user_id:
                user = users_collection.find_one({"_id": ObjectId(user_id)})
        
        
        return {
            "id": str(updated_category["_id"]),
            "name": updated_category["name"],
            "user_id": updated_category["user_id"],
            "user": {
                "name": user["name"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@categoriesRouter.delete("/{category_id}")
async def delete_category(category_id: str, authUser: User = Depends(get_current_user)):
    try:
        result = categories_collection.delete_one({"_id": ObjectId(category_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"message": "Category deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoriesRouter.get("/")
async def get_category_by_user(authUser: User = Depends(get_current_user)):
    try:
        categories = list(categories_collection.find({"user_id": authUser["_id"]}))
        if not categories:
            raise HTTPException(status_code=404, detail="Categories not found")
        
        for category in categories:
            category["_id"] = str(category["_id"])
            category["id"] = str(category["_id"])
        return categories
       
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@categoriesRouter.get("/admin")
async def get_categories_admin(authUser: User = Depends(get_current_admin_user)):
    try:
        categories = list(categories_collection.find())
        if not categories:
            raise HTTPException(status_code=404, detail="Categories not found")
        
        for category in categories:
            user_id = category.get("user_id")
            if user_id:
                user = users_collection.find_one({"_id": ObjectId(user_id)})
                user["_id"] = str(user["_id"])
                user["id"] = str(user["_id"])
            if category:
                category["user"] = user 
            category["_id"] = str(category["_id"])
            category["id"] = str(category["_id"])
            
            
        return categories
    

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
