from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import SessionLocal
from fornecedorservice import AuthService, FornecedorService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from typing import List
import models

SECRET = "your-secret-key"
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
manager = LoginManager(SECRET, token_url="/login", use_cookie=True)
manager.cookie_name = "auth"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@manager.user_loader
def load_user(email: str, db: Session = Depends(get_db)):
    return db.query(models.Fornecedor).filter(models.Fornecedor.email == email).first()

class FornecedorCreate(BaseModel):
    nome: str
    cpf: str
    telefone: str
    senha: str
    email: EmailStr

@router.post("/register", response_model=FornecedorCreate, status_code=status.HTTP_201_CREATED)
def register(fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.create(fornecedor)

@router.post("/login")
def login(response: Response, data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    access_token = manager.create_access_token(data={"sub": user.email})
    manager.set_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("auth")
    return {"msg": "Successfully logged out"}

@router.get("/protected")
def protected_route(user=Depends(manager)):
    return {"msg": f"Hello, {user.email}"}

# @router.post("/fornecedor", response_model=FornecedorCreate, status_code=status.HTTP_201_CREATED)
# def create_fornecedor(fornecedor: FornecedorCreate, db: Session = Depends(get_db), user=Depends(manager)):
#     fornecedor_service = FornecedorService(db)
#     return fornecedor_service.create(fornecedor)

@router.get("/fornecedor", response_model=List[FornecedorCreate], status_code=status.HTTP_200_OK)
def get_all_fornecedores(db: Session = Depends(get_db), user=Depends(manager)):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.get_all()

@router.get("/fornecedor/{fornecedor_id}", response_model=FornecedorCreate, status_code=status.HTTP_200_OK)
def get_single_fornecedor(fornecedor_id: int, db: Session = Depends(get_db), user=Depends(manager)):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.get_by_id(fornecedor_id)

@router.put("/fornecedor/{fornecedor_id}", response_model=FornecedorCreate, status_code=status.HTTP_202_ACCEPTED)
def update_fornecedor(fornecedor_id: int, fornecedor: FornecedorCreate, db: Session = Depends(get_db), user=Depends(manager)):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.update(fornecedor_id, fornecedor)

@router.delete("/fornecedor/{fornecedor_id}", response_model=FornecedorCreate, status_code=status.HTTP_200_OK)
def delete_fornecedor(fornecedor_id: int, db: Session = Depends(get_db), user=Depends(manager)):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.delete(fornecedor_id)
