
<<<<<<< HEAD
from fastapi import Depends, FastAPI, HTTPException
=======
from fastapi import Depends,APIRouter, HTTPException
>>>>>>> db conn
from requests import Session
from app.src.api.v1.users.model.users import User
from app.database.database import get_db
from app.src.api.v1.users.schema.userschemas import StudentCreate, StudentResponse, TeacherCreate, TeacherResponse, TeacherSalary
from app.src.api.v1.users.user_authentication.auth import authorize_admin, get_password_hash

<<<<<<< HEAD
app = FastAPI()

# REQUIREMENT: Add Student (Admin Only)
@app.post("/add_student", response_model=StudentResponse, tags=["add by admin"])
=======
router = APIRouter()

# REQUIREMENT: Add Student (Admin Only)
@router.post("/add_student", response_model=StudentResponse)
>>>>>>> db conn
def add_student(student: StudentCreate, db: Session = Depends(get_db), token: str = Depends(authorize_admin)):

    db_student = db.query(User).filter(User.username == student.username).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Student already added")

    
    hashed_password = get_password_hash(student.password)
    new_student = User(username=student.username, email=student.email, hashed_password=hashed_password, role="student" , class_name=student.class_name)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return new_student


# REQUIREMENT: Add Teacher (Admin Only)
<<<<<<< HEAD
@app.post("/add_teacher", response_model=TeacherResponse, tags=["add by admin"])
=======
@router.post("/add_teacher", response_model=TeacherResponse)
>>>>>>> db conn
def add_teacher(teacher: TeacherCreate, db: Session = Depends(get_db), token: str = Depends(authorize_admin)):

    db_teacher = db.query(User).filter(User.username == teacher.username).first()
    if db_teacher:
        raise HTTPException(status_code=400, detail="Teacher already added")
    
    hashed_password = get_password_hash(teacher.password)
    new_teacher = User(username=teacher.username, email=teacher.email, hashed_password=hashed_password, role="teacher",class_name=teacher.class_name,subject_name=teacher.subject_name)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    
    return  new_teacher


# REQUIREMENT:Add teacher salary by admin
<<<<<<< HEAD
@app.post("/add_salary/{teacher_id}" , tags=["add by admin"])
=======
@router.post("/add_salary/{teacher_id}" )
>>>>>>> db conn
def add_teacher_salary(teacher_id: int, salary: TeacherSalary, db: Session = Depends(get_db), current_user: User = Depends(authorize_admin) ):
    teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()

    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    teacher.salary = salary.salary
    db.commit()
    db.refresh(teacher)

    return {"message": "Salary added successfully", "salary": teacher.salary}