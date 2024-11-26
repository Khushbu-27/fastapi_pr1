
<<<<<<< HEAD
from fastapi import Depends, FastAPI, HTTPException , status
=======
from fastapi import Depends, APIRouter, HTTPException , status
>>>>>>> db conn
from requests import Session
from app.database.database import get_db
from app.src.api.v1.users.model.users import User
from app.src.api.v1.users.schema.userschemas import StudentResponse
from app.src.api.v1.users.user_authentication.auth import authorize_user

<<<<<<< HEAD
app = FastAPI()


# REQUIREMENT: Student - View Own Info
@app.get("/student/{student_id}", response_model=StudentResponse, tags=["student"])
=======
router = APIRouter()


# REQUIREMENT: Student - View Own Info
@router.get("/student/{student_id}", response_model=StudentResponse)
>>>>>>> db conn
def view_own_student_info(current_user= Depends(authorize_user), db: Session = Depends(get_db)):

    if current_user.role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student authorization required")
    
    student = db.query(User).filter(User.username == current_user.username).first()
    return student
