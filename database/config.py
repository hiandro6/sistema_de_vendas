from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session
from database.models import Clientes,Vendas,VendasProdutos,Produtos,Base
engine = create_engine('sqlite:///database/teste.db')
session = Session(bind=engine)

def start_db():
    Base.metadata.create_all(bind=engine)