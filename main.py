from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes import router as fornecedor_router
from routes_servico import router as servico_router
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import models
import auth
from auth import get_current_user

app = FastAPI()
app.include_router(auth.router)
app.include_router(fornecedor_router)
app.include_router(servico_router)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado")
    return {"User": user}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"], 
)

