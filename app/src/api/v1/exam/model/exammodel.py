
from sqlalchemy import Column, Date, Enum, Integer, String
from app.database.database import Base
from sqlalchemy.orm import relationship 
import enum


class ExamStatus(enum.Enum):
    completed = "completed"
    scheduled = "scheduled"

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(Integer, nullable=False)
    subject_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(ExamStatus), nullable=False , default=ExamStatus.scheduled)
    marks = Column(Integer, nullable=False)

    marks_received = relationship(
        "StudentMarks",
        primaryjoin="foreign(StudentMarks.exam_id) == Exam.id",
        back_populates="exam",
        viewonly=True,
    )
