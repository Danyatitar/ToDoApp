import re
from datetime import date, timedelta

import psycopg2
# from auth import authRouter
from fastapi import FastAPI
from sqlalchemy import (Column, Date, Enum, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, validates

Base = declarative_base()
POSTGRESQL_DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/todoapp"

engine = create_engine(
    POSTGRESQL_DATABASE_URL, pool_pre_ping=True
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    role = Column(Enum('admin','user', name='role_enum'))
    

    
    @validates('name')
    def validate_name(self, key, name):
        if len(name) < 4:
            raise ValueError("Category name must be at least 4 characters long")
        return name


    tasks = relationship("Task", back_populates="user")
    categories = relationship("Category", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    deadline = Column(Date)
    status =  Column(Enum('in progress', 'completed', 'waiting', name='status_enum'))
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
    
    @validates('title')
    def check_title_length(self, key, v):
        if len(v) < 4:
            raise ValueError('Title must be at least 4 characters long')
        return v

    @validates('deadline')
    def check_deadline(self, key, v):
        if v < date.today():
            raise ValueError("Deadline must be later than or equal to today's date")
        return v

    @validates('status')
    def check_status(self, key, v):
        valid_statuses = ['in progress', 'completed', 'waiting']
        if v not in valid_statuses:
            raise ValueError('Invalid status. Must be one of: "in progress", "completed", "waiting"')
        return v

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    
    tasks = relationship("Task", back_populates="category")
    user = relationship("User", back_populates="categories")
    
    
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




