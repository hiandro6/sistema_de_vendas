from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey, Date
from typing import List
from database import Base

class VendaProdutos(Base):
    __tablename__ = 'tb_vendas_produtos'
    
    vpr_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vpr_ven_id: Mapped[int] = mapped_column(ForeignKey('tb_vendas.ven_id'))
    vpr_pro_id: Mapped[int] = mapped_column(ForeignKey('tb_produtos.pro_id'))
    vpr_quantproduto: Mapped[int] = mapped_column(nullable=False)
    vpr_precoproduto: Mapped[float] = mapped_column(nullable=False)


    #Produtos não vendidos: Lista os produtos que não foram vendidos nos últimos 7, 30, 60 e 90 dias.
    #SELECT pro_nome FROM tb_produtos JOIN tb_vendas ON pro_id = vpr_pro_id WHERE vpr_datavenda BETWEEN curdate AND curdate - interval 7 day 