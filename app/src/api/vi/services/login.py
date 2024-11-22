
from requests import Session

from app.src.api.vi.user_auth.auth import get_password_hash
from . import models,schemas
from fastapi import FastAPI, Depends, HTTPException

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
