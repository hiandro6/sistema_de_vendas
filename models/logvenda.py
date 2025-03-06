from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey, text
from typing import List
from database import Base
from database import session

class LogVenda(Base):
    __tablename__ = 'tb_logs_vendas'
    
    id_log = mapped_column(primary_key=True, autoincrement=True)
    operacao = mapped_column(String(10), nullable=False)  # Pode ser 'INSERT', 'UPDATE' ou 'DELETE'
    id_venda = mapped_column(Integer, ForeignKey('tb_vendas.ven_id'), nullable=False)
    id_cliente = mapped_column(Integer, ForeignKey('tb_clientes.cli_id'), nullable=False)
    usuario = mapped_column(String(50), nullable=False)
    data_hora = mapped_column(DateTime, nullable=False, default=datetime.utcnow)  # Data e hora da ação

    # Relacionamento com a tabela tb_vendas e tb_clientes
    venda = relationship("Venda", back_populates="logs_vendas")
    cliente = relationship("Cliente", back_populates="logs_vendas")