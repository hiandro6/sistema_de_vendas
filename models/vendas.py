from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey, text
from typing import List
from database import Base
from .vendasprodutos import VendaProdutos
from database.config import session


class Venda(Base):
    __tablename__ = 'tb_vendas'
    ven_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ven_data: Mapped[str] = mapped_column(nullable=False)
    ven_total: Mapped[float] = mapped_column(nullable=False)
    ven_cli_id: Mapped[int] = mapped_column(ForeignKey('tb_clientes.cli_id'))
    clientes: Mapped[List["Cliente"]] = relationship("Cliente", back_populates='vendas')
    #produtos: Mapped[List['VendaProdutos']] = relationship(back_populates='vendas')

    @classmethod
    def find(cls, **kwargs):
        if 'id' in kwargs:
            return session.query(cls).filter_by(ven_id=kwargs['id']).first() #SELECT * FROM tb_vendas WHERE ven_id = id
        else:
            raise AttributeError('A busca deve ser feita por id.')

    @classmethod
    def all(cls, ordem = "crescente"):
        if ordem == "crescente":
            direcao = "ASC"
        elif ordem == "decrescente":
            direcao = "DESC"
        sql = text(f"SELECT * FROM tb_vendas JOIN tb_clientes ON ven_cli_id = cli_id ORDER BY ven_data {direcao}")
        vendas = session.execute(sql).fetchall()
        return vendas

