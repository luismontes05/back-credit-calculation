from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi import Request
from pydantic import BaseModel
from config.database import engine, Base, Session
from models.user import User
from models.company import Company
from routers.user import user_router
from middlewares.error_handler import error_handler
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
app.title = "Backend Software Credit Calculation"
app.version = "0.0.1"
app.include_router(user_router)
app.add_middleware(error_handler)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello, welcome to applications for software developer calculation credit</h1>')