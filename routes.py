import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import SessionLocal
from fornecedorservice import AuthService, FornecedorService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from typing import List
from typing import Annotated

from auth import get_current_user

import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class FornecedorCreate(BaseModel):
    nome: str
    cpf: str
    telefone: str
    senha: str
    email: EmailStr

# @router.post("/register", response_model=FornecedorCreate, status_code=status.HTTP_201_CREATED)
# async def register(fornecedor: FornecedorCreate, db: db_dependency):
#     fornecedor_service = FornecedorService(db)
#     fornecedor.senha = bcrypt_context.hash(fornecedor.senha)
#     created_fornecedor = fornecedor_service.create(fornecedor)
#     return created_fornecedor


@router.post("/fornecedor", response_model=FornecedorCreate, status_code=status.HTTP_201_CREATED)
def create_fornecedor(fornecedor: FornecedorCreate, db: db_dependency):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.create(fornecedor)


@router.get("/fornecedor", response_model=List[FornecedorCreate], status_code=status.HTTP_200_OK)
def get_all_fornecedores(user: user_dependency, db: db_dependency):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.get_all()

@router.get("/fornecedor/{fornecedor_id}", response_model=FornecedorCreate, status_code=status.HTTP_200_OK)
def get_single_fornecedor(fornecedor_id: int, user: user_dependency, db: db_dependency):
    if fornecedor_id != user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para acessar este fornecedor.")
    
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.get_by_id(fornecedor_id)


@router.put("/fornecedor/{fornecedor_id}", response_model=FornecedorCreate, status_code=status.HTTP_202_ACCEPTED)
def update_fornecedor(fornecedor_id: int, fornecedor: FornecedorCreate, user: user_dependency, db: db_dependency):
    if fornecedor_id != user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para atualizar este fornecedor.")
    
    fornecedor_service = FornecedorService(db)
    try:
        updated_fornecedor = fornecedor_service.update(fornecedor_id, fornecedor)
        return updated_fornecedor
    except HTTPException as exc:
        raise exc


@router.delete("/fornecedor/{fornecedor_id}", response_model=FornecedorCreate, status_code=status.HTTP_200_OK)
def delete_fornecedor(fornecedor_id: int, user: user_dependency, db: db_dependency):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.delete(fornecedor_id)
