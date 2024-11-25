
from datetime import time
import random
from fastapi import Depends, FastAPI, HTTPException
from requests import Session
from app.src.api.v1.users.services.utils import email_utils 
from app.database.database import get_db
from app.src.api.v1.users.model.users import User
from app.src.api.v1.users.user_authentication.auth import get_password_hash

app = FastAPI()

otp_store = {}
otp_expiry_time = 300 

#forgot password
@app.post("/forgot-password/" , tags=["login"])
def forgot_password(email: str , db: Session = Depends(get_db)):
    """Generate OTP and send it to the email."""
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user email")

    otp = str(random.randint(100000, 999999))  
    otp_store[email] = {"otp": otp, "timestamp": time.time()}
    
    email_utils.send_otp_email(email, otp)  
    return {"message": "OTP sent to email"}

#reset password
@app.post("/reset-password/", tags=["login"])
def reset_password(user_id: int, email: str, otp: str, new_password: str, db: Session = Depends(get_db)):
    """Verify user ID, OTP and reset password."""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user ID or email")

    if email not in otp_store:
        raise HTTPException(status_code=400, detail="OTP not requested")
    
    otp_data = otp_store[email]

    if time.time() - otp_data["timestamp"] > otp_expiry_time:
        del otp_store[email]
        raise HTTPException(status_code=400, detail="OTP expired")
    
    if otp_data["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.commit()

    del otp_store[email]
    
    return {"message": "Password reset successful"}
