
<<<<<<< HEAD
from fastapi import Depends, FastAPI, HTTPException , status
=======
from fastapi import Depends, APIRouter, HTTPException , status
>>>>>>> db conn
from requests import Session
from app.database.database import get_db
from app.src.api.v1.users.model.users import User
from app.src.api.v1.users.schema.userschemas import AdminResponse, StudentResponse, TeacherResponse
from app.src.api.v1.users.user_authentication.auth import authorize_admin

<<<<<<< HEAD
app = FastAPI()

# REQUIREMENT: View Admin own Info
@app.get("/admin/{admin_id}", response_model=AdminResponse, tags=["admin"])
=======
router = APIRouter()

# REQUIREMENT: View Admin own Info
@router.get("/admin/{admin_id}", response_model=AdminResponse)
>>>>>>> db conn
def view_admin_info(admin_id: int, token: dict = Depends(authorize_admin), db: Session = Depends(get_db), current_user = Depends(authorize_admin)):

    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    
    return admin

# REQUIREMENT: Admin - View Student Info
<<<<<<< HEAD
@app.get("/admin/view_student/{student_id}", response_model=StudentResponse, tags=["admin"])
=======
@router.get("/admin/view_student/{student_id}", response_model=StudentResponse)
>>>>>>> db conn
def admin_view_student_info(student_id: int, token: str = Depends(authorize_admin), db: Session = Depends(get_db)):

    student = db.query(User).filter(User.id == student_id, User.role == "student").first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


# REQUIREMENT: Admin - View Teacher Info
<<<<<<< HEAD
@app.get("/admin/view_teacher/{teacher_id}", response_model=TeacherResponse, tags=["admin"])
=======
@router.get("/admin/view_teacher/{teacher_id}", response_model=TeacherResponse)
>>>>>>> db conn
def admin_view_teacher_info(teacher_id: int, token: str = Depends(authorize_admin), db: Session = Depends(get_db)):

    teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher


# REQUIREMENT: View Teacher Salary by admin
<<<<<<< HEAD
@app.get("/view_teacher_salary/{teacher_id}", tags=["admin"])
=======
@router.get("/view_teacher_salary/{teacher_id}")
>>>>>>> db conn
def view_teacher_salary(
    teacher_id: int, db: Session = Depends(get_db), current_user: User = Depends(authorize_admin)):
  
    teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()

    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    if teacher.salary is None:
        raise HTTPException(status_code=404, detail="Salary not set for this teacher")

    return {"teacher_id": teacher.id, "salary": teacher.salary}