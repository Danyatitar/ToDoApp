
from fastapi import APIRouter, Depends, HTTPException
from middleware import (get_current_admin_user, get_current_user,
                        get_db_connection)
from models import CategoryCreate, CategoryUpdateAdmin
from schemas import Category, User

conn = get_db_connection()


categoriesRouter = APIRouter()


@categoriesRouter.post("/")
async def create_category(category_data: CategoryCreate, authUser: User = Depends(get_current_user)):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO categories (name, user_id) VALUES (%s, %s) RETURNING id",
                (category_data.name, authUser.id)
            )
            new_category_id = cur.fetchone()[0]
            conn.commit()
        
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM categories WHERE id = %s", (new_category_id,))
            new_category = cur.fetchone()
        result = {
            "id": new_category[0],
            "name": new_category[1],
            "user_id": new_category[2]
        }
        return result
        
        return new_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoriesRouter.post("/admin")
async def create_category_admin(category_data: CategoryUpdateAdmin, authUser: User = Depends(get_current_user)):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO categories (name, user_id) VALUES (%s, %s) RETURNING id",
                (category_data.name, category_data.user_id)
            )
            new_category_id = cur.fetchone()[0]
            conn.commit()
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM categories JOIN users on users.id = categories.user_id WHERE categories.id = %s", (new_category_id,))
            new_category = cur.fetchone()
        
        
        return {
            "id": new_category[0],
            "name": new_category[1],
            "user_id": new_category[2],
            "user":{
                "name": new_category[4]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoriesRouter.patch("/{category_id}")
async def update_category(category_id: int, category_data: CategoryCreate, authUser: User = Depends(get_current_user)):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE categories SET name = %s WHERE id = %s AND user_id = %s",
                (category_data.name, category_id, authUser.id)
            )
            conn.commit()
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
            updated_category = cur.fetchone()
            
        result = {
            "id": updated_category[0],
            "name": updated_category[1],
            "user_id": updated_category[2]
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoriesRouter.patch("/admin/{category_id}")
async def update_category_admin(category_id: int, category_data: CategoryUpdateAdmin, authUser: User = Depends(get_current_user)):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE categories SET name = %s, user_id = %s WHERE id = %s",
                (category_data.name, category_data.user_id, category_id)
            )
            conn.commit()
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM categories JOIN users on users.id = categories.user_id WHERE categories.id = %s", (category_id,))
            updated_category = cur.fetchone()
        
        
        return {
            "id": updated_category[0],
            "name": updated_category[1],
            "user_id": updated_category[2],
            "user":{
                "name": updated_category[4]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoriesRouter.delete("/{category_id}")
async def delete_category(category_id: int):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM categories WHERE id = %s", (category_id,))
            conn.commit()
        
        return {"message": "Category deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoriesRouter.get("/")
async def get_category_by_user(authUser: User = Depends(get_current_user)):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM categories WHERE user_id = %s", (authUser.id,))
            categories = cur.fetchall()

        if not categories:
            raise HTTPException(status_code=404, detail="Categories not found")
        result = [
            {
                "id": category[0],
                "name": category[1],
                "user_id": category[2]
            }
            for category in categories
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoriesRouter.get("/admin")
async def get_categories_admin(authUser: User = Depends(get_current_admin_user)):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM categories JOIN users on users.id = categories.user_id")
            categories = cur.fetchall()

        if not categories:
            raise HTTPException(status_code=404, detail="Categories not found")
        
        result = [
            {
                "id": category[0],
                "name": category[1],
                "user_id": category[2],
                "user": {
                    "name": category[4]
                }
            }
            for category in categories
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
