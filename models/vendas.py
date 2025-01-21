from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey
from typing import List
from database import Base

class Vendas(Base):
    __tablename__ = 'tb_vendas'
    ven_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ven_data: Mapped[str] = mapped_column(nullable=False)
    ven_total: Mapped[float] = mapped_column(nullable=False)
    ven_cli_id: Mapped[int] = mapped_column(ForeignKey('tb_clientes.cli_id'))

    produtos: Mapped[List['VendasProdutos']] = relationship(back_populates='vendas')
