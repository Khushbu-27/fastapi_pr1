
from fastapi import Depends, APIRouter, HTTPException
from requests import Session
from app.database.database import get_db
from app.src.api.v1.exam.model.exammodel import Exam
from app.src.api.v1.users.user_authentication.auth import authorize_user

router= APIRouter()

# REQUIREMENT: teacher can delete exam
@router.delete("/teacher/delete_exam/{exam_id}")
def delete_exam(exam_id: int, current_user=Depends(authorize_user), db: Session = Depends(get_db)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can delete exams")
    
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    if current_user.role == "teacher":
        if exam.class_name != current_user.class_name or exam.subject_name != current_user.subject_name:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this exam schedule.")

    db.delete(exam)
    db.commit()
    
    return {"message": "Exam deleted successfully"}