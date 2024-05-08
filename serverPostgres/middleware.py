from typing import Optional

import psycopg2
from fastapi import Cookie, Depends, Header, HTTPException, Path
from helper import decode_token
from models import TaskUpdate
from psycopg2 import Error
from schemas import Category, Task, User


def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="todoapp",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
    )
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def close_db_connection(connection):
    if connection:
        connection.close()

def decode_refresh_token(refresh_token: Optional[str] = Cookie(None, alias="refresh_token"), connection = Depends(get_db_connection)):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Access denied")
    
    payload = decode_token(refresh_token)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (payload["email"],))
        user_record = cursor.fetchone()
        if user_record is None:
            raise HTTPException(status_code=404, detail="User not found")

        user = User(id=user_record[0], name = user_record[1],email=user_record[2], role=user_record[4]) # Assuming your user table has (id, email, role) columns
        return user
    except Error as e:
        print(f"Error fetching user from database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        cursor.close()

def get_current_user(authorization: Optional[str] = Header(None), connection = Depends(get_db_connection)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access denied")
    
    access_token = authorization.split("Bearer ")[1]

    payload = decode_token(access_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (payload["email"],))
        user_record = cursor.fetchone()
        if user_record is None:
            raise HTTPException(status_code=404, detail="User not found")

        user = User(id=user_record[0], email=user_record[1], role=user_record[2]) # Assuming your user table has (id, email, role) columns
        return user
    except Error as e:
        print(f"Error fetching user from database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        cursor.close()

def get_current_admin_user(authorization: Optional[str] = Header(None), connection = Depends(get_db_connection)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access denied")
    
    access_token = authorization.split("Bearer ")[1]

    payload = decode_token(access_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s AND role = 'admin'", (payload["email"],))
        user_record = cursor.fetchone()
        if user_record is None:
            raise HTTPException(status_code=404, detail="User not found or not an admin")

        user = User(id=user_record[0], email=user_record[1], role=user_record[2]) # Assuming your user table has (id, email, role) columns
        return user
    except Error as e:
        print(f"Error fetching user from database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        cursor.close()

def check_task(task_id: int = Path(..., title="The ID of the task to retrieve"), current_user: User = Depends(get_current_user), connection = Depends(get_db_connection)) -> Task:
    cursor = connection.cursor()
    try:
        if current_user.role == 'admin':
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        else:
            cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, current_user.id))
        
        task_record = cursor.fetchone()
        if task_record is None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task = Task(id=task_record[0], name=task_record[1], user_id=task_record[2]) # Assuming your task table has (id, name, user_id) columns
        return task
    except Error as e:
        print(f"Error fetching task from database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        cursor.close()

def check_category(category_id: int = Path(..., title="The ID of the category to retrieve"), current_user: User = Depends(get_current_user), connection = Depends(get_db_connection)) -> Category:
    cursor = connection.cursor()
    try:
        if current_user.role == 'admin':
            cursor.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
        else:
            cursor.execute("SELECT * FROM categories WHERE id = %s AND user_id = %s", (category_id, current_user.id))
        
        category_record = cursor.fetchone()
        if category_record is None:
            raise HTTPException(status_code=404, detail="Category not found")
        
        category = Category(id=category_record[0], name=category_record[1], user_id=category_record[2]) # Assuming your category table has (id, name, user_id) columns
        return category
    except Error as e:
        print(f"Error fetching category from database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        cursor.close()


