from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional
from database import SessionLocal
from models import Servico
from service_servico import ServicoService
from auth import get_current_user  # Certifique-se de importar a função get_current_user corretamente
from typing import Annotated

import os
import base64
from io import BytesIO
from PIL import Image
import uuid
router = APIRouter()
db = SessionLocal()
servico_service = ServicoService(db)

class ServicoBase(BaseModel):
    nome: str
    descricao: str
    preco: str
    imagem: str

class ServicoCreate(ServicoBase):
    pass  # Removemos fornecedor_id daqui

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
def create_servico(
    servico: ServicoBase,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    try:
        fornecedor_id = current_user["id"]
        imagem_data = servico.imagem.split(",")[1]  # Remove o prefixo "data:image/jpeg;base64," para obter apenas os dados base64
        imagem_bytes = base64.b64decode(imagem_data)
        
        # Gerar um nome aleatório para a imagem
        imagem_nome = f"{uuid.uuid4()}.jpg"
        
        # Caminho para o diretório de imagens de serviços
        diretorio_imagens = "/imagem/servicos"
        
        # Garantir que o diretório exista
        if not os.path.exists(diretorio_imagens):
            os.makedirs(diretorio_imagens)
        
        # Salvar a imagem em um arquivo temporário
        caminho_imagem = os.path.join(diretorio_imagens, imagem_nome)
        with open(caminho_imagem, "wb") as file:
            file.write(imagem_bytes)
        
        # Criar uma instância do objeto Servico com o caminho da imagem temporária
        novo_servico = Servico(
            nome=servico.nome,
            descricao=servico.descricao,
            preco=servico.preco,
            imagem=caminho_imagem,  # Caminho da imagem temporária
            fornecedor_id=fornecedor_id
        )
        
        # Agora você pode salvar o novo_servico no banco de dados
        
        return servico_service.create(novo_servico)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
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
