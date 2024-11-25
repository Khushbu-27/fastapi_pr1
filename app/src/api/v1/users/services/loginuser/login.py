from datetime import date
from fastapi.security import OAuth2PasswordRequestForm
from requests import Session

from app.database.database import get_db
from app.src.api.v1.users.user_authentication import get_password_hash
from app.src.api.v1.users.user_authentication.auth import create_access_token, verify_password
from . import models,schemas
from fastapi import FastAPI, Depends, HTTPException , status

app = FastAPI()


# REQUIREMENT: Registration for Admin only
@app.post("/admin/register", response_model=schemas.AdminResponse, tags=["admin"])
def admin_register(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    """
    Register an admin after validating email and ensuring it is valid.
    """
    if admin.password != admin.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and confirm password do not match"
        )
    
    if db.query(models.User).filter(models.User.username == admin.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    if db.query(models.User).filter(models.User.email == admin.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(admin.password)
    new_admin = models.User(
        username=admin.username,
        email=admin.email,
        hashed_password=hashed_password,
        role="admin"
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    return {
        "message": "Your email has been verify. You can login with your username",
        "id": new_admin.id,
        "username": new_admin.username,
        "email": new_admin.email
    }


# REQUIREMENT: Login users
@app.post('/login', tags=["login"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):   
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    today = date.today()

    if user.role == "admin":
        access_token = create_access_token(data={"sub": user.username, "role": "admin"})
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "role": "admin",
            "message": "Admin login successful"
        }

    elif user.role in ["teacher", "student"]:
        
        if user.last_login_date != today:
            user.attendance += 1
            user.last_login_date = today    
        db.commit() 

        access_token = create_access_token(data={"sub": user.username, "role": user.role})
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "role": user.role,
            "attendance": user.attendance,  
            "message": f"{user.role.capitalize()} login successful"
        }