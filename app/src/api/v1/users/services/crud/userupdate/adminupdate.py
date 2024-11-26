
<<<<<<< HEAD
from fastapi import Depends, FastAPI, HTTPException
=======
from fastapi import Depends, APIRouter, HTTPException
>>>>>>> db conn
from requests import Session
from app.database.database import get_db
from app.src.api.v1.users.model.users import User
from app.src.api.v1.users.schema.userschemas import TeacherSalary
from app.src.api.v1.users.user_authentication.auth import authorize_admin

<<<<<<< HEAD
app = FastAPI()

# REQUIREMENT: update teacher salary by admin
@app.put("/admin/update_salary/{teacher_id}", tags=["admin"])
=======
router = APIRouter()

# REQUIREMENT: update teacher salary by admin
@router.put("/admin/update_salary/{teacher_id}")
>>>>>>> db conn
def update_teacher_salary(
    teacher_id: int,
    salary: TeacherSalary, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(authorize_admin)
):
    
    teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()

    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    if teacher.salary is None:
        raise HTTPException(status_code=400, detail="Teacher salary must be set first before updating")

    teacher.salary = salary.salary
    db.commit()
    db.refresh(teacher)

    return {"message": "Teacher salary updated successfully", "teacher_id": teacher.id, "salary": teacher.salary}