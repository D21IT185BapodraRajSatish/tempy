from fastapi import APIRouter,HTTPException, Request
import json
from app.models.user_model import User
from app.utils.password_handler import verify_password  # Assume this is the hashing function
from app.auth.jwt_handler import create_access_token  # Your JWT creation logic

router = APIRouter()

@router.post("/token")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    user = User.get_user(username)

    if not user or not verify_password(password, user['password']):  
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}
