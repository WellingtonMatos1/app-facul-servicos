import bcrypt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import models
import re
from email_validator import validate_email, EmailNotValidError


class FornecedorService:
    def __init__(self, db):
        self.db = db
        self.auth_service = AuthService(db)

    def is_valid_name(self, name: str) -> bool:
        return bool(re.match(r"^[a-zA-Z\s]+$", name))

    def is_valid_cpf(self, cpf: str) -> bool:
        return len(cpf) == 11 and cpf.isdigit()

    def is_valid_phone(self, phone: str) -> bool:
        return len(phone) in [10, 11] and phone.isdigit()

    def is_valid_email(self, email: str) -> bool:
        try:
            validate_email(email)
            return True
        except EmailNotValidError as e:
            raise HTTPException(status_code=422, detail=f"E-mail inválido: {str(e)}")

    def get_all(self):
        return self.db.query(models.Fornecedor).all()

    def get_by_id(self, fornecedor_id: int):
        fornecedor = self.db.query(models.Fornecedor).filter(models.Fornecedor.id == fornecedor_id).first()
        if fornecedor:
            return fornecedor
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado")

    def create(self, fornecedor):
        if not self.is_valid_name(fornecedor.nome):
            raise HTTPException(status_code=422, detail="Nome inválido. Deve conter apenas letras e espaços.")

        if not self.is_valid_cpf(fornecedor.cpf):
            raise HTTPException(status_code=422, detail="CPF inválido. Deve conter 11 dígitos numéricos sem caracteres especiais.")

        if not self.is_valid_phone(fornecedor.telefone):
            raise HTTPException(status_code=422, detail="Telefone inválido. Deve ter 10 ou 11 dígitos.")

        if not self.is_valid_email(fornecedor.email):
            raise HTTPException(status_code=422, detail="E-mail inválido.")

        if self.db.query(models.Fornecedor).filter(models.Fornecedor.cpf == fornecedor.cpf).first():
            raise HTTPException(status_code=409, detail="CPF já cadastrado.")

        if self.db.query(models.Fornecedor).filter(models.Fornecedor.email == fornecedor.email).first():
            raise HTTPException(status_code=409, detail="E-mail já cadastrado.")

        hashed_password = self.auth_service.get_password_hash(fornecedor.senha)
        new_fornecedor = models.Fornecedor(
            nome=fornecedor.nome,
            cpf=fornecedor.cpf,
            telefone=fornecedor.telefone,
            senha=hashed_password,
            email=fornecedor.email
        )

        self.db.add(new_fornecedor)
        self.db.commit()
        self.db.refresh(new_fornecedor)
        return new_fornecedor

    def update(self, fornecedor_id: int, fornecedor):
        find_fornecedor = self.db.query(models.Fornecedor).filter(models.Fornecedor.id == fornecedor_id).first()
        if not find_fornecedor:
            raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")

        if fornecedor.nome and not self.is_valid_name(fornecedor.nome):
            raise HTTPException(status_code=422, detail="Nome inválido. Deve conter apenas letras e espaços.")

        if fornecedor.cpf and not self.is_valid_cpf(fornecedor.cpf):
            raise HTTPException(status_code=422, detail="CPF inválido. Deve conter 11 dígitos numéricos sem caracteres especiais.")

        if fornecedor.telefone and not self.is_valid_phone(fornecedor.telefone):
            raise HTTPException(status_code=422, detail="Telefone inválido. Deve ter 10 ou 11 dígitos.")

        if fornecedor.email and not self.is_valid_email(fornecedor.email):
            raise HTTPException(status_code=422, detail="E-mail inválido.")

        if fornecedor.cpf and self.db.query(models.Fornecedor).filter(
            models.Fornecedor.cpf == fornecedor.cpf,
            models.Fornecedor.id != fornecedor_id,
        ).first():
            raise HTTPException(status_code=409, detail="CPF já em uso por outro fornecedor.")

        if fornecedor.email and self.db.query(models.Fornecedor).filter(
            models.Fornecedor.email == fornecedor.email,
            models.Fornecedor.id != fornecedor_id,
        ).first():
            raise HTTPException(status_code=409, detail="E-mail já em uso por outro fornecedor.")

        if fornecedor.senha:
            hashed_password = self.auth_service.get_password_hash(fornecedor.senha)
            find_fornecedor.senha = hashed_password

        if fornecedor.nome:
            find_fornecedor.nome = fornecedor.nome
        if fornecedor.cpf:
            find_fornecedor.cpf = fornecedor.cpf
        if fornecedor.telefone:
            find_fornecedor.telefone = fornecedor.telefone
        if fornecedor.email:
            find_fornecedor.email = fornecedor.email

        self.db.commit()
        self.db.refresh(find_fornecedor)
        return find_fornecedor


    def delete(self, fornecedor_id: int):
        find_fornecedor = self.db.query(models.Fornecedor).filter(models.Fornecedor.id == fornecedor_id).first()
        if find_fornecedor:
            self.db.delete(find_fornecedor)
            self.db.commit()
            return find_fornecedor
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado")

from fastapi import HTTPException, status

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def verify_password(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def get_password_hash(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def authenticate_user(self, email: str, password: str):
        user = self.db.query(models.Fornecedor).filter(models.Fornecedor.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        if not self.verify_password(password, user.senha):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha incorreta")
        return user

