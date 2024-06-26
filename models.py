from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine


def create_tables():
    Base.metadata.create_all(engine)


class Fornecedor(Base):
    __tablename__ = 'fornecedores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(40), nullable=False)
    cpf = Column(String(11), nullable=False)
    telefone = Column(String(11), nullable=False)
    senha = Column(String(120), nullable=False)
    email = Column(String(80), nullable=False)
    servicos = relationship('Servico', backref='fornecedores', cascade="all, delete-orphan", single_parent=True)


class Servico(Base):
    __tablename__ = 'servico'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(40), nullable=False)
    descricao = Column(String(100), nullable=False)
    preco = Column(String(40), nullable=False)
    imagem = Column(String(100), nullable=False)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'), nullable=False)
