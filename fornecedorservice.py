from fastapi import HTTPException, status
from database import SessionLocal
import models

class FornecedorService:
    def __init__(self, db):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(models.Fornecedor).all()

    def get_by_id(self, fornecedor_id):
        fornecedor = self.db.query(models.Fornecedor).filter(models.Fornecedor.id == fornecedor_id).first()
        if fornecedor:
            return fornecedor
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id do Fornecedor não encontrado")

    def create(self, fornecedor):
        new_fornecedor = models.Fornecedor(
            nome=fornecedor.nome,
            cpf=fornecedor.cpf,
            telefone=fornecedor.telefone,
            senha=fornecedor.senha,
            email=fornecedor.email
        )
        self.db.add(new_fornecedor)
        self.db.commit()
        self.db.refresh(new_fornecedor)
        return new_fornecedor

    def update(self, fornecedor_id, fornecedor):
        find_fornecedor = self.db.query(models.Fornecedor).filter(models.Fornecedor.id == fornecedor_id).first()
        if find_fornecedor:
            find_fornecedor.nome = fornecedor.nome
            find_fornecedor.cpf = fornecedor.cpf
            find_fornecedor.telefone = fornecedor.telefone
            find_fornecedor.senha = fornecedor.senha
            find_fornecedor.email = fornecedor.email
            self.db.commit()
            return find_fornecedor
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id do Fornecedor não encontrado")

    def delete(self, fornecedor_id):
        find_fornecedor = self.db.query(models.Fornecedor).filter(models.Fornecedor.id == fornecedor_id).first()
        if find_fornecedor:
            self.db.delete(find_fornecedor)
            self.db.commit()
            return find_fornecedor
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado")
