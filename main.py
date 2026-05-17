from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/greet")
def greet():
    return {"message": "Hello, welcome to FastAPI!"}

# Path parameter example
@app.get("/greet/{name}")
def greet_name(name: str):
    return {"message": f"Hello, {name}! Welcome to FastAPI!"}

# Query parameter example
@app.get("/greet/")
def greet_query(name: str = "World", age: int = 0):
    return {"message": f"Hello, {name}! You are {age} years old. Welcome to FastAPI!"}

# Query parameter with Optional parameter
@app.get("/greet_user/{name}")
def greet_user(name: str, age: Optional[int] = None):
    if age is None:
        return {"message": f"Hello, {name}! Welcome to FastAPI!"}
    return {"message": f"Hello, {name}! You are {age} years old. Welcome to FastAPI!"}


# Post request example
class Student(BaseModel):
    name: str
    age: int
    rollNo: int

# This endpoint will accept a JSON body with the student's details and return the same details in the response.
@app.post("/create_student")
def create_student(student: Student):
    return {
        "name": student.name,
        "age": student.age,
        "rollNo": student.rollNo
    }