from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session
from models.clientes import Clientes
from models.produtos import Produtos
from models.vendas import Vendas
from models.vendasprodutos import VendasProdutos
from database import Base


engine = create_engine('sqlite:///database/teste.db')
session = Session(bind=engine)

def start_db():
    Base.metadata.create_all(bind=engine)