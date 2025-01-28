from flask import Blueprint, redirect, url_for, request, render_template
from models.vendas import Venda
from models.clientes import Cliente
from models.produtos import Produto
from models.vendasprodutos import VendaProdutos
from sqlalchemy import text
from database.config import session

relatorios_bp = Blueprint(name='relatorio', import_name=__name__, template_folder='templates', url_prefix='/relatorios')

relatorios_bp.route('/', methods=['GET', 'POST'])
def filtros():
    if request.method == 'POST':
        sql = text("""SELECT pro_nome FROM tb_produtos WHERE pro_id NOT IN (
		SELECT vpr_pro_id FROM tb_vendas_produtos
		JOIN tb_vendas ON vpr_ven_id = ven_id
		WHERE ven_data >= CURDATE() - INTERVAL 7 DAY);""")
        consulta = session.execute(sql)
        pass
    else:
        return render_template("relatorios/filtros.html", produtos = consulta)

#linha 192 de vendas
#linha 192 de vendas
#linha 192 de vendas
#linha 192 de vendas
#linha 192 de vendas
#linha 192 de vendaskkkkkkkkkkk