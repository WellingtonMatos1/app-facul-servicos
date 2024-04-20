from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from database import SessionLocal
from models import Servico
from typing import List
from fornecedorservice import FornecedorService


import models
from fornecedorservice import FornecedorService

router = APIRouter()
db = SessionLocal()
fornecedor_service = FornecedorService(db)

class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True

class Fornecedor(BaseModel):
    nome: str
    cpf: str
    telefone: str
    senha: str
    email: EmailStr

@router.get('/fornecedor', response_model=list[Fornecedor], status_code=status.HTTP_200_OK)
def get_all_fornecedores():
    return fornecedor_service.get_all()

@router.get('/fornecedor/{fornecedor_id}', response_model=Fornecedor, status_code=status.HTTP_200_OK)
def get_single_fornecedor(fornecedor_id: int):
    return fornecedor_service.get_by_id(fornecedor_id)

@router.post('/fornecedor', response_model=Fornecedor, status_code=status.HTTP_201_CREATED)
def add_fornecedor(fornecedor: Fornecedor):
    return fornecedor_service.create(fornecedor)

@router.put('/fornecedor/{fornecedor_id}', response_model=Fornecedor, status_code=status.HTTP_202_ACCEPTED)
def update_fornecedor(fornecedor_id: int, fornecedor: Fornecedor):
    return fornecedor_service.update(fornecedor_id, fornecedor)

@router.delete('/fornecedor/{fornecedor_id}', response_model=Fornecedor, status_code=status.HTTP_200_OK)
def delete_fornecedor(fornecedor_id: int):
    return fornecedor_service.delete(fornecedor_id)
