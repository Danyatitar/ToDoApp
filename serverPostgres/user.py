import psycopg2
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path
from middleware import (get_current_admin_user, get_current_user,
                        get_db_connection)
from models import UserCreateAdmin, UserUpdate, UserUpdateAdmin
from schemas import User

userRouter = APIRouter()
conn = get_db_connection()

@userRouter.patch("/")
async def update_user(user_data: UserUpdate, authUser: User = Depends(get_current_user)):
    try:
        

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET name = %s WHERE id = %s",
                (user_data.name, authUser.id)
            )
            conn.commit()


        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (authUser.id,))
            updated_user = cur.fetchone()
        result = {
            "id": updated_user[0],
            "email": updated_user[2],
            "name": updated_user[1],
            "role": updated_user[4]
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.patch("/admin/{user_id}")
async def update_user_admin(user_data: UserUpdateAdmin, user_id: int = Path(..., title="User ID"), authUser: User = Depends(get_current_user)):
    try:

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET name = %s, email = %s, role = %s WHERE id = %s",
                (user_data.name, user_data.email, user_data.role, user_id)
            )
            conn.commit()


        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            updated_user = cur.fetchone()

        result = {
            "id": updated_user[0],
            "email": updated_user[2],
            "name": updated_user[1],
            "role": updated_user[4]
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.post("/admin")
async def create_user(user_data: UserCreateAdmin, authUser: User = Depends(get_current_admin_user)):
    try:

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (email, password, name, role) VALUES (%s, %s, %s, %s) RETURNING id",
                (user_data.email, user_data.password, user_data.name, user_data.role)
            )
            new_user_id = cur.fetchone()[0]
            conn.commit()

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (new_user_id,))
            new_user = cur.fetchone()

        result = {
            "id": new_user[0],
            "email": new_user[2],
            "name": new_user[1],
            "role": new_user[4]
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.get("/")
async def get_user(authUser: User = Depends(get_current_user)):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (authUser.id,))
            user = cur.fetchone()
        result = {
            "id": user[0],
            "email": user[2],
            "name": user[1],
            "role": user[4]
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.get("/admin")
async def get_users_admin(authUser: User = Depends(get_current_admin_user)):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

        if not users:
            raise HTTPException(status_code=404, detail="Users not found")
        
        result = [
            {
                "id": user[0],
                "email": user[2],
                "name": user[1],
                "role": user[4]
            }
            for user in users
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.delete("/{user_id}")
async def delete_user(user_id: int = Path(..., title="User ID"), authUser: User = Depends(get_current_admin_user)):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
        
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
