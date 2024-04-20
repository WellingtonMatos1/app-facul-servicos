from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
from database import SessionLocal
from models import Servico
from service_servico import ServicoService
from typing import Optional



router = APIRouter()
db = SessionLocal()
servico_service = ServicoService(db)

class ServicoBase(BaseModel):
    nome: str
    descricao: str
    preco: str
    imagem: str

class ServicoCreate(ServicoBase):
    fornecedor_id: int

class ServicoUpdate(ServicoBase):
    nome: Optional[str]
    descricao: Optional[str]
    preco: Optional[str]
    imagem: Optional[str]

class ServicoOut(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: str
    imagem: str

@router.get("/servico", response_model=List[ServicoOut], status_code=status.HTTP_200_OK)
def get_all_servicos():
    return servico_service.get_all()


@router.get("/fornecedor/{fornecedor_id}/servicos", response_model=List[ServicoOut], status_code=status.HTTP_200_OK)
def get_servicos_by_fornecedor(fornecedor_id: int):
    return servico_service.get_by_fornecedor_id(fornecedor_id)

@router.get("/servico/{servico_id}", response_model=ServicoOut, status_code=status.HTTP_200_OK)
def get_servico(servico_id: int):
    return servico_service.get_by_id(servico_id)

@router.post("/servico", response_model=ServicoOut, status_code=status.HTTP_201_CREATED)
def create_servico(servico: ServicoCreate):
    return servico_service.create(servico)

@router.put("/servico/{servico_id}", response_model=ServicoOut, status_code=status.HTTP_200_OK)
def update_servico(servico_id: int, servico: ServicoUpdate):
    return servico_service.update(servico_id, servico)

@router.delete("/servico/{servico_id}", response_model=ServicoOut, status_code=status.HTTP_200_OK)
def delete_servico(servico_id: int):
    return servico_service.delete(servico_id)
