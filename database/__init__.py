from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text

from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///database/teste.db')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass
try:
    def create_trigger_verificar_estoque():
        sql_trigger_verificar_estoque = """
        CREATE TRIGGER verificar_estoque
        BEFORE INSERT ON tb_vendas_produtos
        FOR EACH ROW
        BEGIN
            -- Verifica se o estoque é suficiente para a quantidade
            -- Se o estoque for insuficiente, a trigger será abortada
            SELECT
                CASE
                    WHEN (SELECT pro_estoque FROM tb_produtos WHERE pro_id = NEW.vpr_pro_id) < NEW.vpr_quantproduto
                    THEN RAISE (ABORT, 'Estoque insuficiente para o produto')
                END;
        END;
        """

        session.execute(text(sql_trigger_verificar_estoque))
        session.commit()
    def check_and_create_trigger():

        result = session.execute(text("SELECT name FROM sqlite_master WHERE type='trigger'")).fetchall()
            
        if not result:
            create_trigger_verificar_estoque()

    check_and_create_trigger()
except:
    pass