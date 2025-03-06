from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey, Date, text
from typing import List
from database import Base
from database import session


class VendaProdutos(Base):
    __tablename__ = 'tb_vendas_produtos'
    
    vpr_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vpr_ven_id: Mapped[int] = mapped_column(ForeignKey('tb_vendas.ven_id'))
    vpr_pro_id: Mapped[int] = mapped_column(ForeignKey('tb_produtos.pro_id'))
    vpr_quantproduto: Mapped[int] = mapped_column(nullable=False)
    vpr_precoproduto: Mapped[float] = mapped_column(nullable=False)

    #venda: Mapped["Venda"] = relationship("Venda", back_populates="produtos")

    #Produtos não vendidos: Lista os produtos que não foram vendidos nos últimos 7, 30, 60 e 90 dias.
    #SELECT pro_nome FROM tb_produtos JOIN tb_vendas ON pro_id = vpr_pro_id WHERE vpr_datavenda BETWEEN curdate AND curdate - interval 7 day 

    @classmethod
    def find(cls, **kwargs):
        if 'ven_id' in kwargs:
            sql = text("SELECT * FROM tb_vendas_produtos WHERE vpr_ven_id = :id")
            vendapro = session.execute(sql, {"id": kwargs['ven_id']}).fetchone()
        elif 'vpr_id' in kwargs:
            #return session.query(cls).filter_by(pro_id=kwargs['id']).first()
            sql = text("SELECT * FROM tb_vendas_produtos WHERE vpr_id = :id ")
            vendapro = session.execute(sql, {"id": kwargs['vpr_id']}).fetchone()
        else:
            raise AttributeError('A busca deve ser feita por id.')
        return vendapro