from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth_database import get_db, Base, engine
import models, schemas, utils
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

# 
SECRET_KEY = "9557f196c178960719259570092b18901e7d6888382d9901b12dd4290026bade"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Creating helper function to create access token
def create_access_token(data: dict):
    to_encode = data.copy()

    # You can add an expiration time to the token if needed
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Register user endpoint
@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Hash the password
    hashed_password = utils.hash_password(user.password)

    # Create new user
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    # Add user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create access token
    # access_token = create_access_token(data={"sub": new_user.id})

    # return {"access_token": access_token, "token_type": "bearer"}

    # Return the created user details (excluding password)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role
    }


# Login user endpoint   
@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify password
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Create access token
    access_token = create_access_token(data={"sub": user.id})

    return {"access_token": access_token, "token_type": "bearer"}