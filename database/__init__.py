from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text

from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///database/teste.db')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass

def create_trigger_verificar_estoque():
    sql_trigger_verificar_estoque = """
    CREATE TRIGGER verificar_estoque
    BEFORE INSERT ON tb_vendas_produtos
    FOR EACH ROW
    BEGIN
        DECLARE estoque_atual INT;
        
        SELECT pro_estoque INTO estoque_atual 
        FROM tb_produtos 
        WHERE pro_id = NEW.vpr_pro_id;

        IF estoque_atual < NEW.vpr_quantproduto THEN
            RAISE (ABORT, 'Estoque insuficiente para o produto');
        END IF;
    END;
    """
def check_and_create_trigger():
    with engine.connect() as connection:

        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='trigger'")).fetchall()
        
        if not result:
            create_trigger_verificar_estoque()

check_and_create_trigger()