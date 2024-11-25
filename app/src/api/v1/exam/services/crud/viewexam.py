
from fastapi import Depends, APIRouter, HTTPException, status
from requests import Session
from app.database.database import get_db
from app.src.api.v1.exam.model.exammodel import Exam
from app.src.api.v1.users.user_authentication.auth import authorize_user

router = APIRouter()


#REQUIREMENT: teacher and student view exam schedule
@router.get("/exam/{exam_id}", status_code=status.HTTP_200_OK)
def view_exam_schedule(
    exam_id: int,
    current_user=Depends(authorize_user),  
    db: Session = Depends(get_db)
):
    
    if current_user.role not in ["student", "teacher"]:
        raise HTTPException(status_code=403, detail="Only students and teachers can view exam schedules.")

    exam = db.query(Exam).filter(Exam.id == exam_id).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found.")

    if current_user.role == "teacher":
        if exam.class_name != current_user.class_name or exam.subject_name != current_user.subject_name:
            raise HTTPException(status_code=403, detail="You are not authorized to view this exam schedule.")
    
    elif current_user.role == "student":
        if exam.class_name != current_user.class_name:
            raise HTTPException(status_code=403, detail="You are not authorized to view this exam schedule.")

    return exam