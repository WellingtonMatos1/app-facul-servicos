from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

nome_banco = "trab"
usuario_postgres = "postgres"
senha_postgres = "senha_aqui"
host_postgres = "localhost"
porta_postgres = "5432"

connection_string = f"postgresql://{usuario_postgres}:{senha_postgres}@{host_postgres}:{porta_postgres}/{nome_banco}"

engine = create_engine(connection_string, pool_pre_ping=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
