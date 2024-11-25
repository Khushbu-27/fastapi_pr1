
from fastapi import Depends, FastAPI, HTTPException ,status
from requests import Session
from app.database.database import get_db
from app.src.api.v1.users.model.users import User
from app.src.api.v1.users.schema.userschemas import StudentResponse, TeacherResponse, TeacherSalary
from app.src.api.v1.users.user_authentication.auth import authorize_user

app = FastAPI()

# REQUIREMENT: Teacher - View Own Info
@app.get("/teacher/{teacher_id}", response_model=TeacherResponse, tags=["teacher"])
def view_own_teacher_info(db: Session = Depends(get_db) , current_user=Depends(authorize_user)):

    if current_user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher authorization required")
    
    teacher = db.query(User).filter(User.username == current_user.username).first()
    return teacher


# REQUIREMENT: view teacher own salary
@app.get("/teacher/view_salary/{teacher_id}" , tags=["teacher"],response_model=TeacherSalary)
def view_my_salary( db: Session = Depends(get_db), current_user = Depends(authorize_user)):
   
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Not authorized to view this salary")
    
    salary = db.query(User).filter(User.salary == current_user.salary).first()

    if current_user.salary is None:
        raise HTTPException(status_code=404, detail="Salary not set for this teacher")

    return {"teacher_id": current_user.id, "salary": salary}


# REQUIREMENT: Teacher - View Student Info (View Only)
@app.get("/teacher/view_student/{student_id}", response_model=StudentResponse, tags=["teacher"])
def teacher_view_student_info(student_id: int, current_user = Depends(authorize_user), db: Session = Depends(get_db)):

    if current_user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher authorization required")
    
    student = db.query(User).filter(User.id == student_id, User.role == "student").first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student