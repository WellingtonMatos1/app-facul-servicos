from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

nome_banco = "trab"
senha_postgres = "aqui"

connection_string = f"postgresql://postgres:{senha_postgres}@localhost/{nome_banco}"

engine = create_engine(connection_string, pool_pre_ping=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
