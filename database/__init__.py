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
    print("função criada com sucesso")

sql_procedure = """
    CREATE PROCEDURE validar_venda(
        IN id_cliente INT,
        IN id_produto INT,
        IN quantidade INT
    )
    BEGIN
        DECLARE estoque_atual INT;
        DECLARE status_cliente VARCHAR(50);
        DECLARE data_atual DATE;

        -- Verifica o estoque do produto
        SELECT pro_estoque INTO estoque_atual
        FROM tb_produtos
        WHERE pro_id = id_produto;

        IF estoque_atual < quantidade THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Estoque insuficiente para o produto';
        END IF;

        -- Verifica o status do cliente
        SELECT cli_status INTO status_cliente
        FROM tb_clientes
        WHERE cli_id = id_cliente;

        IF status_cliente != 'ativo' THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cliente não está apto para realizar a compra';
        END IF;

        -- Verifica a data da venda (exemplo: não pode ser uma data futura)
        SET data_atual = CURDATE();

        IF data_atual > CURDATE() THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Data da venda inválida';
        END IF;

        -- Se todas as validações passarem, insere a venda
        INSERT INTO tb_vendas (ven_cli_id, ven_pro_id, ven_quantidade, ven_data)
        VALUES (id_cliente, id_produto, quantidade, CURDATE());

        -- Atualiza o estoque do produto
        UPDATE tb_produtos
        SET pro_estoque = pro_estoque - quantidade
        WHERE pro_id = id_produto;

        -- Retorna uma mensagem de sucesso
        SELECT 'Venda realizada com sucesso!' AS mensagem;
    END;"""    

def criar_procedure():
    print("procedure criado com sucesso")

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
    criar_procedure()
    print("deu bom o procedure")
    
except:
    print('quebrou o trigger ou a funcao D:')
