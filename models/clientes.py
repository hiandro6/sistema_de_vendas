from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey, text
from sqlalchemy.exc import NoResultFound

from typing import List
from database import Base
from flask_login import UserMixin
from database.config import session
from .vendas import Venda

class Cliente(Base, UserMixin):
    __tablename__ = 'tb_clientes'
    cli_id:Mapped[int] = mapped_column(primary_key = True, autoincrement=True)
    cli_nome:Mapped[str] = mapped_column(nullable=False)
    cli_email:Mapped[str] = mapped_column(unique = True, nullable=False)
    cli_telefone:Mapped[str] = mapped_column(nullable=False)
    cli_endereco:Mapped[str] = mapped_column(nullable=False)
    vendas: Mapped[list["Venda"]] = relationship("Venda", back_populates="clientes")

    @classmethod
    def find(cls, **kwargs):
        if 'email' in kwargs:
            sql = text("SELECT * FROM tb_clientes WHERE cli_email = :email")
            cliente = session.execute(sql, {"email": kwargs['email']}).fetchone()
        elif 'id' in kwargs:
            sql = text("SELECT * FROM tb_clientes WHERE cli_id = :id")
            cliente = session.execute(sql, {"id": kwargs['id']}).fetchone()
        else:
            raise AttributeError('A busca deve ser feita por email ou id.')
        return cliente


    @classmethod
    def all(cls, ordem = "crescente"):
        if ordem == "crescente":
            direcao = "ASC"
        elif ordem == "decrescente":
            direcao = "DESC"
        sql = text(f"SELECT * FROM tb_clientes ORDER BY cli_nome {direcao}")
        clientes = session.execute(sql).fetchall()
        return clientes