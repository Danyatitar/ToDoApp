import psycopg2
from fastapi import APIRouter, Depends, HTTPException
from helper import hash_password
from middleware import (get_current_admin_user, get_current_user,
                        get_db_connection)
from models import TaskCreate, TaskCreateAdmin, TaskUpdate, TaskUpdateAdmin
from schemas import Task, User

conn = get_db_connection()


tasksRouter = APIRouter()


@tasksRouter.post("/")
async def create_task(task_data: TaskCreate, authUser: User = Depends(get_current_user)):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title, description, deadline, status, user_id, category_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                (task_data.title, task_data.description, task_data.deadline, task_data.status, authUser.id, task_data.category_id)
            )
            new_task_id = cur.fetchone()[0]
            conn.commit()
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s", (new_task_id,))
            new_task = cur.fetchone()
        result = {
            "id": new_task[0],
            "title": new_task[1],
            "description": new_task[2],
            "deadline": new_task[3],
            "status": new_task[4],
            "category_id": new_task[6],
            "user_id": new_task[5]
        }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tasksRouter.post("/admin")
async def create_task_admin(task_data: TaskCreateAdmin, authUser: User = Depends(get_current_admin_user)):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title, description, deadline, status, user_id, category_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                (task_data.title, task_data.description, task_data.deadline, task_data.status, task_data.user_id, task_data.category_id)
            )
            new_task_id = cur.fetchone()[0]
            conn.commit()
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks JOIN categories ON tasks.category_id = categories.id JOIN users ON users.id = tasks.user_id WHERE tasks.id = %s", (new_task_id,))
            new_task = cur.fetchone()
        
        result = {
            "id": new_task[0],
            "title": new_task[1],
            "description": new_task[2],
            "deadline": new_task[3],
            "status": new_task[4],
            "category_id": new_task[6],
            "user_id": new_task[5],
            "category":{
                "id": new_task[7],
                "name": new_task[8]
            },
            "user":{
                "id": new_task[10],
                "name": new_task[11],
                "email": new_task[12],
                "role": new_task[14]
            }
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tasksRouter.put("/{task_id}")
async def update_task(task_id: int, task_data: TaskUpdate, authUser: User = Depends(get_current_user)):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET title = %s, description = %s, deadline = %s, status = %s, category_id = %s WHERE id = %s AND user_id = %s",
                (task_data.title, task_data.description, task_data.deadline, task_data.status, task_data.category_id, task_id, authUser.id)
            )
            conn.commit()
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks JOIN categories ON tasks.category_id = categories.id WHERE tasks.id = %s", (task_id,))
            updated_task = cur.fetchone()
        result = {
            "id": updated_task[0],
            "title": updated_task[1],
            "description": updated_task[2],
            "deadline": updated_task[3],
            "status": updated_task[4],
            "category_id": updated_task[6],
            "user_id": updated_task[5],
            "category": {
                    "id": updated_task[7],
                    "name": updated_task[8]
                }
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tasksRouter.put("/admin/{task_id}")
async def update_task_admin(task_id: int, task_data: TaskUpdateAdmin, authUser: User = Depends(get_current_admin_user)):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET title = %s, description = %s, deadline = %s, status = %s, category_id = %s, user_id = %s WHERE id = %s",
                (task_data.title, task_data.description, task_data.deadline, task_data.status, task_data.category_id, task_data.user_id, task_id)
            )
            conn.commit()
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks JOIN categories ON tasks.category_id = categories.id JOIN users ON users.id = tasks.user_id WHERE tasks.id = %s", (task_id,))
            updated_task = cur.fetchone()
        
        result = {
            "id": updated_task[0],
            "title": updated_task[1],
            "description": updated_task[2],
            "deadline": updated_task[3],
            "status": updated_task[4],
            "category_id": updated_task[6],
            "user_id": updated_task[5],
            "category":{
                "id": updated_task[7],
                "name": updated_task[8]
            },
            "user":{
                "id": updated_task[10],
                "name": updated_task[11],
                "email": updated_task[12],
                "role": updated_task[14]
            }
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tasksRouter.delete("/{task_id}")
async def delete_task(task_id: int):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            conn.commit()
        
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tasksRouter.get("/")
async def get_task_by_user(authUser: User = Depends(get_current_user)):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks JOIN categories ON tasks.category_id = categories.id WHERE tasks.user_id = %s", (authUser.id,))
            tasks = cur.fetchall()
            print(tasks)
            

        if not tasks:
            raise HTTPException(status_code=404, detail="Tasks not found")
        result = [
            {
                "id": task[0],
                "title": task[1],
                "description": task[2],
                "deadline": task[3],
                "status": task[4],
                "category_id": task[6],
                "user_id": task[5],
                "category":{
                    "id": task[7],
                    "name": task[8]
                }
            }
            for task in tasks
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tasksRouter.get("/admin")
async def get_tasks_admin(authUser: User = Depends(get_current_admin_user)):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks JOIN categories ON tasks.category_id = categories.id JOIN users ON users.id = tasks.user_id")
            tasks = cur.fetchall()

        if not tasks:
            raise HTTPException(status_code=404, detail="Tasks not found")

        result = [
            {
                "id": task[0],
                "title": task[1],
                "description": task[2],
                "deadline": task[3],
                "status": task[4],
                "category_id": task[6],
                "user_id": task[5],
                "category":{
                    "id": task[7],
                    "name": task[8]
                },
                "user":{
                    "id": task[10],
                    "name": task[11],
                    "email": task[12],
                    "role": task[14]
                }
            }
            for task in tasks
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
