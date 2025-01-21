from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey
from typing import List
from database import Base

class Produtos(Base):
    __tablename__ = 'tb_produtos'
    
    pro_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pro_nome: Mapped[str] = mapped_column(nullable=False)
    pro_descricao: Mapped[str] = mapped_column(nullable=False)
    pro_preco: Mapped[float] = mapped_column(nullable=False)
    pro_estoque: Mapped[int] = mapped_column()

    vendas: Mapped[List['VendasProdutos']] = relationship(back_populates='produtos')