from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey
from typing import List
from database import Base
from flask_login import UserMixin

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
        if 'email' in kwargs.keys():
            res = conn.execute("SELECT * from users where email = ?", (kwargs['email'],))
        elif 'id' in kwargs.keys():
            res = conn.execute("SELECT * from users where id = ?", (kwargs['id'],))
        else:
            raise AttributeError('A busca deve ser feita por email ou id.')
        data = res.fetchone()
        if data:
            user = User(nome=data['nome'], email=data['email'])
            user.id = data['id']
            return user
        return None