from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text

from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///database/teste.db')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass

calcular_total_vendas = """
CREATE FUNCTION calcular_total_vendas(id_cliente INTEGER, data_inicio TEXT, data_fim TEXT)
RETURNS REAL
BEGIN
    DECLARE total_vendas REAL;

    -- Calcula o total de vendas para o cliente no intervalo de datas
    SELECT COALESCE(SUM(ven_total), 0) INTO total_vendas
    FROM tb_vendas
    WHERE ven_cli_id = id_cliente
    AND ven_data BETWEEN date(data_inicio) AND date(data_fim);

    -- Retorna o total de vendas
    RETURN total_vendas;
END;
"""

def criar_funcao_calcular_total_vendas():
    print("eeebaaaaaa")

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

log_trigger_insert = f"""
        -- Trigger para INSERT
        CREATE TRIGGER log_vendas_insert
        AFTER INSERT ON tb_vendas
        FOR EACH ROW
        BEGIN
            INSERT INTO tb_logs_vendas (log_operacao, log_id_venda, log_id_cliente, log_usuario, log_data_hora)
            VALUES ('INSERT', NEW.ven_id, NEW.ven_cli_id, NEW.ven_usuario, CURRENT_TIMESTAMP);
        END;
        """

log_trigger_update = """
        -- Trigger para UPDATE
        CREATE TRIGGER log_vendas_update
        AFTER UPDATE ON tb_vendas
        FOR EACH ROW
        BEGIN
            INSERT INTO tb_logs_vendas (log_operacao, log_id_venda, log_id_cliente, log_usuario, log_data_hora)
            VALUES ('UPDATE', NEW.ven_id, NEW.ven_cli_id, NEW.ven_usuario, CURRENT_TIMESTAMP);
        END;
    """

log_trigger_delete = """
        -- Trigger para DELETE
        CREATE TRIGGER log_vendas_delete
        AFTER DELETE ON tb_vendas
        FOR EACH ROW
        BEGIN
            INSERT INTO tb_logs_vendas (log_operacao, log_id_venda, log_id_cliente, log_usuario, log_data_hora)
            VALUES ('DELETE', OLD.ven_id, OLD.ven_cli_id, OLD.ven_usuario, CURRENT_TIMESTAMP);
        END;
        """

def check_and_create_trigger():

        result = session.execute(text("SELECT name FROM sqlite_master WHERE type='trigger'")).fetchall()
            
        if not result:
            session.execute(text(sql_trigger_verificar_estoque))
            session.execute(text(log_trigger_insert))
            session.execute(text(log_trigger_update))
            session.execute(text(log_trigger_delete))
            session.commit()

try:
    check_and_create_trigger()
    print("deu bom o trigger")
    criar_funcao_calcular_total_vendas()
    print("deu bom a função")
except:
    print('quebrou o trigger ou a funcao D:')
