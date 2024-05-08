import re
from datetime import datetime

import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb+srv://danylo:qwerty123@cluster0.jthorx6.mongodb.net/?authMechanism=DEFAULT')
db = client['todo_app']
users_collection = db['users']
tasks_collection = db['tasks']
categories_collection = db['categories']

class User:
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
    
    @staticmethod
    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address format")
        return email
    
    @staticmethod
    def validate_name(name):
        if len(name) < 4:
            raise ValueError("Name must be at least 4 characters long")
        return name
    
    @staticmethod
    def validate_role(role):
        if role not in ['admin', 'user']:
            raise ValueError("Invalid role. Must be 'admin' or 'user'")
        return role
    
    def save(self):
        user_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }
        result = users_collection.insert_one(user_data)
        return result.inserted_id

class Task:
    def __init__(self, title, description, deadline, status, user_id, category_id):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.status = status
        self.user_id = user_id
        self.category_id = category_id
    
    @staticmethod
    def validate_title(title):
        if len(title) < 4:
            raise ValueError("Title must be at least 4 characters long")
        return title
    
    @staticmethod
    def validate_deadline(deadline):
        if deadline < datetime.now():
            raise ValueError("Deadline must be later than or equal to today's date")
        return deadline
    
    @staticmethod
    def validate_status(status):
        valid_statuses = ['in progress', 'completed', 'waiting']
        if status not in valid_statuses:
            raise ValueError('Invalid status. Must be one of: "in progress", "completed", "waiting"')
        return status
    
    def save(self):
        task_data = {
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "status": self.status,
            "user_id": self.user_id,
            "category_id": self.category_id
        }
        result = tasks_collection.insert_one(task_data)
        return result.inserted_id

class Category:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
    
    def save(self):
        category_data = {
            "name": self.name,
            "user_id": self.user_id
        }
        result = categories_collection.insert_one(category_data)
        return result.inserted_id
