from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey, text, DateTime, Date
from typing import List
from database import Base
from database import session
from datetime import datetime

class LogVenda(Base):
    __tablename__ = 'tb_logs_vendas'
    
    log_id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    log_operacao:Mapped[str] = mapped_column(nullable=False)  # Pode ser 'INSERT', 'UPDATE' ou 'DELETE'
    log_id_venda:Mapped[int] = mapped_column(nullable=False)
    log_id_cliente:Mapped[int] = mapped_column(nullable=False)
    log_usuario:Mapped[str] = mapped_column(nullable=False)
    log_data_hora:Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)  # Data e hora da ação

    # # Relacionamento com a tabela tb_vendas e tb_clientes
    # venda = relationship("Venda", back_populates="logs_vendas")
    # cliente = relationship("Cliente", back_populates="logs_vendas")

    @classmethod
    def all(cls):
        sql = text(f"SELECT * FROM tb_logs_vendas")
        logs = session.execute(sql).fetchall()
        return logs