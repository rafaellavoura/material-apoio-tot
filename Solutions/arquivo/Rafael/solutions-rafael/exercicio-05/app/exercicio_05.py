from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime, timezone
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/app_db")
engine = create_engine(DATABASE_URL)

class Livro(SQLModel, table=True):
    __tablename__ = "livros"
    
    id: str = Field(primary_key=True)
    titulo: str
    genero: str
    status: str = Field(default="recebido") # recebido, processado ou erro
    arquivo: str | None = None
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    atualizado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

def criar_tabelas():
    SQLModel.metadata.create_all(engine)

def obter_sessao():
    with Session(engine) as session:
        yield session