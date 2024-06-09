from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Fornecedor
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = "SECRET KEY HERE"
ALGORITHM = "HS256"

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    nome: str
    cpf: str
    telefone: str
    senha: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Fornecedor(
        nome=create_user_request.nome,
        senha=bcrypt.hash(create_user_request.senha),
        cpf=create_user_request.cpf,
        telefone=create_user_request.telefone,
        email=create_user_request.email
    )

    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token(user.email, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Fornecedor).filter(Fornecedor.email == username).first()
    if not user:
        return None
    if not bcrypt.verify(password, user.senha):
        return None
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated [str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
