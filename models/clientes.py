from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey
from sqlalchemy.exc import NoResultFound

from typing import List
from database import Base
from flask_login import UserMixin
from database.config import session
from models.vendas import Vendas

class Clientes(Base, UserMixin):
    __tablename__ = 'tb_clientes'
    cli_id:Mapped[int] = mapped_column(primary_key = True, autoincrement=True)
    cli_nome:Mapped[str] = mapped_column(nullable=False)
    cli_email:Mapped[str] = mapped_column(unique = True, nullable=False)
    cli_telefone:Mapped[str] = mapped_column(nullable=False)
    cli_endereco:Mapped[str] = mapped_column(nullable=False)

    vendas: Mapped[List['Vendas']] = relationship(back_populates='cliente')

    @classmethod
    def find(cls, **kwargs): #trocar a sintaxe pra sqlalchemy
        if 'email' in kwargs:
            try:
                return session.query(cls).filter_by(cli_email=kwargs['email']).one()
            except NoResultFound:
                return None
        elif 'id' in kwargs:
            try:
                return session.query(cls).filter_by(cli_id=kwargs['id']).one()
            except NoResultFound:
                return None
        else:
            raise AttributeError('A busca deve ser feita por email ou id.')