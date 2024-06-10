from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil

from database import SessionLocal
from models import Servico
from service_servico import ServicoService
from auth import get_current_user

router = APIRouter()
db = SessionLocal()
servico_service = ServicoService(db)

UPLOAD_FOLDER = "/imagem/servicos/"  # Altere para o caminho correto em seu sistema

class ServicoBase(BaseModel):
    nome: str
    descricao: str
    preco: str

class ServicoCreate(ServicoBase):
    imagem: UploadFile

class ServicoUpdate(ServicoBase):
    nome: Optional[str]
    descricao: Optional[str]
    preco: Optional[str]

class ServicoOut(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: str
    imagem: str

@router.get("/servico", response_model=List[ServicoOut], status_code=status.HTTP_200_OK)
def get_all_servicos():
    try:
        return servico_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/servico/{fornecedor_id}", response_model=List[ServicoOut], status_code=status.HTTP_200_OK)
def get_servicos_by_fornecedor(fornecedor_id: int):
    try:
        servicos = servico_service.get_by_fornecedor_id(fornecedor_id)
        if not servicos:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serviços não encontrados para este fornecedor")
        return servicos
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/servico/{servico_id}", response_model=ServicoOut, status_code=status.HTTP_200_OK)
def get_servico(servico_id: int):
    try:
        servico = servico_service.get_by_id(servico_id)
        if servico is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serviço não encontrado")
        return servico
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/servico", response_model=ServicoOut, status_code=status.HTTP_201_CREATED)
def create_servico(servico: ServicoCreate, current_user: dict = Depends(get_current_user)):
    try:
        fornecedor_id = current_user["id"]
        filename = f"{fornecedor_id}_{servico.imagem.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as image_file:
            shutil.copyfileobj(servico.imagem.file, image_file)

        novo_servico = Servico(
            nome=servico.nome,
            descricao=servico.descricao,
            preco=servico.preco,
            imagem=filename,
            fornecedor_id=fornecedor_id
        )
        return servico_service.create(novo_servico)
    except Exception as e:
        error_msg = f"Erro ao salvar arquivo de imagem: {str(e)}"
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_msg)

@router.put("/servico/{servico_id}", response_model=ServicoOut, status_code=status.HTTP_200_OK)
def update_servico(servico_id: int, servico: ServicoUpdate):
    try:
        updated_servico = servico_service.update(servico_id, servico)
        if updated_servico is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serviço não encontrado")
        return updated_servico
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/servico/{servico_id}", response_model=ServicoOut, status_code=status.HTTP_200_OK)
def delete_servico(servico_id: int):
    try:
        deleted_servico = servico_service.delete(servico_id)
        if deleted_servico is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serviço não encontrado")
        return deleted_servico
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
