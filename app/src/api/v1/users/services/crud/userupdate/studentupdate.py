
from fastapi import Depends, FastAPI, HTTPException ,status
from requests import Session
from app.database.database import get_db
from app.src.api.v1.users.model.users import User
from app.src.api.v1.users.schema.userschemas import StudentResponse, UserUpdate
from app.src.api.v1.users.user_authentication.auth import authorize_user, get_password_hash

app = FastAPI()

# REQUIREMENT: Student - Update Own Info
@app.put("/student/{student-id}/update", response_model=StudentResponse, tags=["student"])
def update_own_info(update_data: UserUpdate, current_user = Depends(authorize_user), db: Session = Depends(get_db)):

    if current_user.role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student authorization required")
    
    student = db.query(User).filter(User.username == current_user.username).first()
    # if update_data.username:
    #     student.username = update_data.username
    if update_data.password:
        student.hashed_password = get_password_hash(update_data.password)
    db.commit()
    db.refresh(student)
    return {"message": "student info updated successfully" , "student": student}