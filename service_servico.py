from fastapi import HTTPException, status
from database import SessionLocal
import models

class ServicoService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.query(models.Servico).all()

    def get_by_id(self, servico_id):
        servico = self.db.query(models.Servico).filter(models.Servico.id == servico_id).first()
        if servico:
            return servico
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id do Serviço não encontrado")

    def create(self, servico):
        if not self.db.query(models.Fornecedor).filter(models.Fornecedor.id == servico.fornecedor_id).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="ID do fornecedor inválido.")

        new_servico = models.Servico(
            nome=servico.nome,
            descricao=servico.descricao,
            preco=servico.preco,
            imagem=servico.imagem,
            fornecedor_id=servico.fornecedor_id
        )
        self.db.add(new_servico)
        self.db.commit()
        self.db.refresh(new_servico)
        return new_servico

    def update(self, servico_id, servico):
        find_servico = self.db.query(models.Servico).filter(models.Servico.id == servico_id).first()
        if find_servico:
            find_servico.nome = servico.nome
            find_servico.descricao = servico.descricao
            find_servico.preco = servico.preco
            find_servico.imagem = servico.imagem
            self.db.commit()
            return find_servico
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id do Serviço não encontrado")

    def delete(self, servico_id):
        find_servico = self.db.query(models.Servico).filter(models.Servico.id == servico_id).first()
        if find_servico:
            self.db.delete(find_servico)
            self.db.commit()
            return find_servico
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serviço não encontrado")
