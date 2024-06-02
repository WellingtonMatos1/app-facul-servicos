from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from database import SessionLocal
from fornecedorservice import FornecedorService
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class FornecedorCreate(BaseModel):
    nome: str
    cpf: str
    telefone: str
    senha: str
    email: EmailStr

@router.post("/fornecedor", response_model=FornecedorCreate, status_code=status.HTTP_201_CREATED)
def create_fornecedor(fornecedor: FornecedorCreate, db: SessionLocal = Depends(get_db)):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.create(fornecedor)

@router.get("/fornecedor", response_model=List[FornecedorCreate], status_code=status.HTTP_200_OK)
def get_all_fornecedores(db: SessionLocal = Depends(get_db)):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.get_all()

@router.get("/fornecedor/{fornecedor_id}", response_model=FornecedorCreate, status_code=status.HTTP_200_OK)
def get_single_fornecedor(fornecedor_id: int, db: SessionLocal = Depends(get_db)):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.get_by_id(fornecedor_id)

@router.put("/fornecedor/{fornecedor_id}", response_model=FornecedorCreate, status_code=status.HTTP_202_ACCEPTED)
def update_fornecedor(fornecedor_id: int, fornecedor: FornecedorCreate, db: SessionLocal = Depends(get_db)):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.update(fornecedor_id, fornecedor)

@router.delete("/fornecedor/{fornecedor_id}", response_model=FornecedorCreate, status_code=status.HTTP_200_OK)
def delete_fornecedor(fornecedor_id: int, db: SessionLocal = Depends(get_db)):
    fornecedor_service = FornecedorService(db)
    return fornecedor_service.delete(fornecedor_id)
