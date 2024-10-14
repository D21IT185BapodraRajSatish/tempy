from fastapi import FastAPI
from app.auth.auth_router import router as auth_router
from app.routes.upload_router import router as upload_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(upload_router, prefix="/file")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Equipment Monitoring API!"}
