from datetime import timedelta

from auth import authRouter
from categories import categoriesRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tasks import tasksRouter
from user import userRouter

ACCESS_TOKEN_EXPIRE_MINUTES = 400
REFRESH_TOKEN_EXPIRE_MINUTES = 10080

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200","http://localhost:49822" ],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin']
)

app.include_router(authRouter)
app.include_router(userRouter, prefix="/user")
app.include_router(tasksRouter, prefix="/tasks")
app.include_router(categoriesRouter, prefix="/category")

# @app.get("/refresh/")
# async def test():
#     print('Hello')
    
