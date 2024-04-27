from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from database import SessionLocal
import models
import re
from email_validator import validate_email, EmailNotValidError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = []
    for error in exc.errors():
        field_path = " -> ".join(map(str, error["loc"]))
        messages.append(f"{field_path}: {error['msg']}")
    
    return JSONResponse(
        status_code=422,
        content={
            "message": "Erro de validação",
            "details": messages,
        },
    )


class FornecedorService:
    def __init__(self, db):
        self.db = db

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

    def update(self, fornecedor_id: int, fornecedor):
        
        find_fornecedor = self.db.query(models.Fornecedor).filter(models.Fornecedor.id == fornecedor_id).first()
        if not find_fornecedor: raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")

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

        if fornecedor.nome:
            find_fornecedor.nome = fornecedor.nome
        if fornecedor.cpf:
            find_fornecedor.cpf = fornecedor.cpf
        if fornecedor.telefone:
            find_fornecedor.telefone = fornecedor.telefone
        if fornecedor.senha:
            find_fornecedor.senha = fornecedor.senha
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
