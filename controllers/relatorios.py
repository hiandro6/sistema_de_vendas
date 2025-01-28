from flask import Blueprint, redirect, url_for, request, render_template, flash
from models.vendas import Venda
from models.clientes import Cliente
from models.produtos import Produto
from models.vendasprodutos import VendaProdutos
from sqlalchemy import text
from database.config import session

relatorio_bp = Blueprint(name='relatorio', import_name=__name__, template_folder='templates', url_prefix='/relatorios')

@relatorio_bp.route('/', methods=['GET', 'POST'])
def filtros():
    consulta = []
    dias = request.form.get("dias", type=int, default=7)
    print("metodo post")
    # Obter o número de dias do formulário

    try:
        # Consultar os produtos que não foram vendidos nos últimos X dias
        sql_mysql = text("""
            SELECT pro_nome, pro_preco, pro_estoque 
            FROM tb_produtos 
            WHERE pro_id NOT IN (
                SELECT vpr_pro_id 
                FROM tb_vendas_produtos
                JOIN tb_vendas ON vpr_ven_id = ven_id
                WHERE ven_data >= CURDATE() - INTERVAL :dias DAY
            )
        """)

        sql_sqlite = text("""
SELECT pro_nome, pro_preco, pro_estoque 
FROM tb_produtos 
WHERE pro_id NOT IN (
    SELECT DISTINCT vpr_pro_id 
    FROM tb_vendas_produtos
    JOIN tb_vendas ON vpr_ven_id = ven_id
    WHERE ven_data >= DATE('now', '-? days')
)
""")
        consulta = session.execute(sql_sqlite, {"dias": dias}).fetchall()
        print(consulta)
    except Exception as e:
        print(f"Erro ao gerar relatório: {str(e)}", "error")
        flash(f"Erro ao gerar relatório: {str(e)}", "error")
    finally:
        return render_template("relatorios/filtros.html", produtos = consulta)
