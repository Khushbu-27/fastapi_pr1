
from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException, Query, status
from requests import Session
from app.database.database import get_db
from app.src.api.v1.exam.model.exammodel import Exam
from app.src.api.v1.users.user_authentication.auth import authorize_user

router = APIRouter()

# REQUIREMENT: add exam by teacher only
@router.post("/exam", status_code=status.HTTP_201_CREATED)
def add_exam_schedule(
    date: str = Query(...),
    status: str = Query(...),
    marks: int = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(authorize_user)
):
   
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can add exams.")
    
    class_name = current_user.class_name
    subject_name = current_user.subject_name
    
    if current_user.class_name != class_name or current_user.subject_name != subject_name:
        raise HTTPException(status_code=403, detail="You cannot add an exam for this class or subject.")

    try:
        exam_date = datetime.strptime(date, "%d-%m-%Y").date() 
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    if exam_date < datetime.today().date():
        raise HTTPException(status_code=400, detail="Exam date cannot be in the past.")
    
    status = status.lower()
    if status not in ['scheduled', 'completed']:
        raise HTTPException(status_code=400, detail="Invalid status. Choose either 'scheduled' or 'completed'.")
    
    existing_exam = db.query(Exam).filter(
            Exam.subject_name == subject_name,
            Exam.date == exam_date
        ).first()
    
    if existing_exam:
            raise HTTPException(status_code=400, detail=f"Exam for this subject have already been added.")

    new_exam = Exam(
        class_name=class_name,
        subject_name=subject_name,
        date=exam_date,
        status=status, 
        marks=marks 
    )
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    return {"message": "Exam added successfully", "exam": new_exam}