from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey
from typing import List

#mapeamento declarativo

class Base(DeclarativeBase):
    pass

class Clientes(Base):
    __tablename__ = 'tb_clientes'
    cli_id:Mapped[int] = mapped_column(primary_key = True, autoincrement=True)
    cli_nome:Mapped[str] = mapped_column(nullable=False)
    cli_email:Mapped[str] = mapped_column(unique = True, nullable=False)
    cli_telefone:Mapped[str] = mapped_column(nullable=False)
    cli_endereco:Mapped[str] = mapped_column(nullable=False)

    vendas: Mapped[List['Vendas']] = relationship(back_populates='cliente')

class Vendas(Base):
    __tablename__ = 'tb_vendas'
    ven_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ven_data: Mapped[str] = mapped_column(nullable=False)
    ven_total: Mapped[float] = mapped_column(nullable=False)
    ven_cli_id: Mapped[int] = mapped_column(ForeignKey('tb_clientes.cli_id'))

    produtos: Mapped[List['VendasProdutos']] = relationship(back_populates='vendas')


class Produtos(Base):
    __tablename__ = 'tb_produtos'
    
    pro_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pro_nome: Mapped[str] = mapped_column(nullable=False)
    pro_descricao: Mapped[str] = mapped_column(nullable=False)
    pro_preco: Mapped[float] = mapped_column(nullable=False)
    pro_estoque: Mapped[int] = mapped_column()

    vendas: Mapped[List['VendasProdutos']] = relationship(back_populates='produtos')


class VendasProdutos(Base):
    __tablename__ = 'tb_vendas_produtos'
    
    vpr_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vpr_ven_id: Mapped[int] = mapped_column(ForeignKey('tb_vendas.ven_id'))
    vpr_pro_id: Mapped[int] = mapped_column(ForeignKey('tb_produtos.pro_id'))
    vpr_quantproduto: Mapped[int] = mapped_column(nullable=False)
    vpr_precoproduto: Mapped[float] = mapped_column(nullable=False)