from fastapi import APIRouter
from app.src.api.v1.exam.services.crud.createexam import router as create_exam_router
from app.src.api.v1.exam.services.crud.deleteexam import router as delete_exam_router
from app.src.api.v1.exam.services.crud.updateexam import router as update_exam_router
from app.src.api.v1.exam.services.crud.viewexam import router as view_exam_router
from app.src.api.v1.marks.services.crud.createmarks import router as create_marks_router
from app.src.api.v1.marks.services.crud.viewmarks import router as view_marks_router
from app.src.api.v1.users.services.crud.usercreate import router as user_create_router
from app.src.api.v1.users.services.crud.userdelete import router as user_delete_router
from app.src.api.v1.users.services.crud.userread.adminview import router as admin_view_router
from app.src.api.v1.users.services.crud.userread.studentview import router as student_view_router
from app.src.api.v1.users.services.crud.userread.teacherview import router as teacher_view_router
from app.src.api.v1.users.services.crud.userupdate.adminupdate import router as admin_update_router
from app.src.api.v1.users.services.crud.userupdate.studentupdate import router as student_update_router
from app.src.api.v1.users.services.crud.userupdate.teacherupdate import router as teacher_update_router
from app.src.api.v1.users.services.loginuser.login import router as login_router
from app.src.api.v1.users.services.loginuser.googlelogin import router as google_login_router

# Centralized Router
router = APIRouter()

# Include routers
router.include_router(create_exam_router, prefix="/exam/create", tags=["Exam"])
router.include_router(delete_exam_router, prefix="/exam/delete", tags=["Exam"])
router.include_router(update_exam_router, prefix="/exam/update", tags=["Exam"])
router.include_router(view_exam_router, prefix="/exam/view", tags=["Exam"])
router.include_router(create_marks_router, prefix="/marks/create", tags=["Marks"])
router.include_router(view_marks_router, prefix="/marks/view", tags=["Marks"])
router.include_router(user_create_router, prefix="/user/create", tags=["User"])
router.include_router(user_delete_router, prefix="/user/delete", tags=["User"])
router.include_router(admin_view_router, prefix="/user/view/admin", tags=["User"])
router.include_router(student_view_router, prefix="/user/view/student", tags=["User"])
router.include_router(teacher_view_router, prefix="/user/view/teacher", tags=["User"])
router.include_router(admin_update_router, prefix="/user/update/admin", tags=["User"])
router.include_router(student_update_router, prefix="/user/update/student", tags=["User"])
router.include_router(teacher_update_router, prefix="/user/update/teacher", tags=["User"])
router.include_router(login_router, prefix="/login", tags=["Authentication"])
router.include_router(google_login_router, prefix="/google-login", tags=["Authentication"])
