
<<<<<<< HEAD
from fastapi import Depends, FastAPI, HTTPException
=======
from fastapi import Depends, APIRouter, HTTPException
>>>>>>> db conn
from requests import Session
from app.src.api.v1.users.model.users import User
from app.database.database import get_db
from app.src.api.v1.users.user_authentication.auth import authorize_user

<<<<<<< HEAD
app = FastAPI()

# REQUIREMENT: admin can delete users
@app.delete("/admin/delete_user/{user_id}" , tags=["admin"])
=======
router = APIRouter()

# REQUIREMENT: admin can delete users
@router.delete("/admin/delete_user/{user_id}" )
>>>>>>> db conn
async def delete_user(user_id: int, current_user=Depends(authorize_user), db: Session = Depends(get_db)):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, details= 'Only admin can delete users')
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}