from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey, text
from typing import List
from database import Base
from .vendasprodutos import VendaProdutos
from database.config import session

class Produto(Base):
    __tablename__ = 'tb_produtos'
    
    pro_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pro_nome: Mapped[str] = mapped_column(nullable=False)
    pro_descricao: Mapped[str] = mapped_column(nullable=False)
    pro_preco: Mapped[float] = mapped_column(nullable=False)
    pro_estoque: Mapped[int] = mapped_column()

    #vendas: Mapped[List['VendaProdutos']] = relationship('VendaProdutos', back_populates='produtos')

    @classmethod
    def estoque(cls, **kwargs):
        if 'nome' in kwargs:
            sql = text("SELECT pro_estoque FROM tb_produtos WHERE pro_nome = :nome")
            produto = session.execute(sql, {"nome": kwargs['nome']}).fetchone()
        elif 'id' in kwargs:
            sql = text("SELECT pro_estoque FROM tb_produtos WHERE pro_id = :id")
            produto = session.execute(sql, {"id": kwargs['id']}).fetchone()
        
        if produto:
            return int(produto[0]) #acessando o valor do estoque(1° item da tupla)
        else:
            return 0

    @classmethod
    def find(cls, **kwargs):
        if 'nome' in kwargs:
            sql = text("SELECT * FROM tb_produtos WHERE pro_nome = :nome")
            produto = session.execute(sql, {"nome": kwargs['nome']}).fetchone()
        elif 'id' in kwargs:
            sql = text("SELECT * FROM tb_produtos WHERE pro_id = :id")
            produto = session.execute(sql, {"id": kwargs['id']}).fetchone()
        else:
            raise AttributeError('A busca deve ser feita por nome ou id.')
        return produto


    @classmethod
    def all(cls, ordem = "crescente"):
        if ordem == "crescente":
            direcao = "ASC"
        elif ordem == "decrescente":
            direcao = "DESC"
        sql = text(f"SELECT * FROM tb_produtos ORDER BY pro_nome {direcao}")
        produtos = session.execute(sql).fetchall()
        return produtos