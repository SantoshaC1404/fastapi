from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.auth_database import get_db, Base, engine
from auth import models, schemas, utils
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError


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
    access_token = create_access_token(data={"sub": str(user.id), "username": user.username, "role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}


# def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login")), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: int = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#     except jwt.JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user



# Dependency to get the current user from the token 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: invalid user id in token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return {"user_id": user.id, "username": user.username, "email": user.email, "role": user.role}


# Protected route example
@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}! This is a protected route."}


# Role-based access control dependency
def require_role(allowed_roles):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")

        if isinstance(allowed_roles, (list, tuple, set)):
            if user_role not in allowed_roles:
                raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
        else:
            if user_role != allowed_roles:
                raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
        return current_user
    return role_checker


# Example of a route that requires admin role
@app.get("/profile")
def profile(current_user: dict = Depends(require_role(["user", "admin"]))):
    return {"message": f"Hello, {current_user['username']}! ({current_user['role']})."}


# Example of a route that requires admin role
@app.get("/admin/dashboard")
def admin_dashboard(current_user: dict = Depends(require_role("admin"))):
    return {"message": f"Hello, {current_user['username']}! This is the admin dashboard."}


# Example of a route that requires user role
@app.get("/user/dashboard")
def user_dashboard(current_user: dict = Depends(require_role("user"))):
    return {"message": f"Hello, {current_user['username']}! This is your dashboard."}
