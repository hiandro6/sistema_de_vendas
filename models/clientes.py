from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey, text
from sqlalchemy.exc import NoResultFound

from typing import List
from database import Base
from flask_login import UserMixin
from database import session
from .vendas import Venda


class Cliente(Base, UserMixin):
    __tablename__ = 'tb_clientes'
    cli_id:Mapped[int] = mapped_column(primary_key = True, autoincrement=True)
    cli_nome:Mapped[str] = mapped_column(nullable=False)
    cli_email:Mapped[str] = mapped_column(unique = True, nullable=False)
    cli_telefone:Mapped[str] = mapped_column(nullable=False)
    cli_endereco:Mapped[str] = mapped_column(nullable=False)
    cli_senha:Mapped[str] = mapped_column(nullable=False)
    cli_tipo:Mapped[str] = mapped_column(nullable=False)
    vendas: Mapped[list["Venda"]] = relationship("Venda", back_populates="clientes", cascade="all, delete-orphan")
    logs_vendas = relationship("LogVenda", back_populates="cliente")


    def get_id(self): #sobresrever get id do UserMixin
        return str(self.cli_id)
    
    @classmethod
    def find(cls, **kwargs):
        if 'email' in kwargs:
            return session.query(cls).filter_by(cli_email=kwargs['email']).first() #SELECT * FROM tb_clientes WHERE cli_email = email
        elif 'id' in kwargs:
            return session.query(cls).filter_by(cli_id=kwargs['id']).first() #SELECT * FROM tb_clientes WHERE cli_id = id
        else: 
            raise AttributeError('A busca deve ser feita por email ou id.')

        """if 'email' in kwargs:
            sql = text("SELECT * FROM tb_clientes WHERE cli_email = :email")
            result = session.execute(sql, {"email": kwargs['email']}).first() #aqui retorna uma tupla, e precisamos retornar um objeto
        elif 'id' in kwargs:
            sql = text("SELECT * FROM tb_clientes WHERE cli_id = :id")
            result = session.execute(sql, {"id": kwargs['id']}).first()
        else:
            raise AttributeError('A busca deve ser feita por email ou id.')
        if result: # então aqui convertemos o resultado da consulta em uma instância de `Cliente`
            return cls(
                cli_id=result.cli_id,
                cli_nome=result.cli_nome,
                cli_email=result.cli_email,
                cli_telefone=result.cli_telefone,
                cli_endereco=result.cli_endereco
            )
        return None"""


    @classmethod
    def all(cls, ordem = "crescente"):
        if ordem == "crescente":
            direcao = "ASC"
        elif ordem == "decrescente":
            direcao = "DESC"
        sql = text(f"SELECT * FROM tb_clientes ORDER BY cli_nome {direcao}")
        clientes = session.execute(sql).fetchall()
        return clientes