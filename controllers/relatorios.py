from flask import Blueprint, redirect, url_for, request, render_template, flash
from models.vendas import Venda
from models.clientes import Cliente
from models.produtos import Produto
from models.vendasprodutos import VendaProdutos
from models.logvenda import LogVenda
from sqlalchemy import text, func, select, desc, or_
from database import session
from flask_login import login_required
from decorators.role import role_required

relatorio_bp = Blueprint(name='relatorio', import_name=__name__, template_folder='templates', url_prefix='/relatorios')

@relatorio_bp.route('/', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def filtros():
    return render_template("relatorios/filtros.html")

@relatorio_bp.route('/totalcompras', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def totalcompras():
    # clientes = []
    if request.method == 'POST':
        data_inicio = request.form.get("data_inicio")
        data_fim = request.form.get("data_fim")
        info_cliente = request.form['id_cliente']
        if info_cliente.isnumeric():  # se o dado for um número fazemos a busca por id, caso contrário buscamos pelo email
            cliente = Cliente.find(id=info_cliente)
        else:
            cliente = Cliente.find(email=info_cliente)

        try:
            if info_cliente:
                # Consulta para contar o total de compras por cliente no período
                cliente_query = (
                    session.query(
                        Cliente.cli_nome,
                        func.count(Venda.ven_id).label('quantidade_compras'),
                        func.sum(Venda.ven_total).label('total_gasto')
                    )
                    .join(Venda, Cliente.cli_id == Venda.ven_cli_id)
                    .filter(Venda.ven_data.between(data_inicio, data_fim), or_(Cliente.cli_id == info_cliente, Cliente.cli_email == info_cliente))  # Filtra pelo intervalo de datas
                    .group_by(Cliente.cli_id)
                    .order_by(desc('quantidade_compras'))  # Ordena pelo número de compras
                )
            else:
                # Consulta para contar o total de compras por cliente no período
                cliente_query = (
                    session.query(
                        Cliente.cli_nome,
                        func.count(Venda.ven_id).label('quantidade_compras'),
                        func.sum(Venda.ven_total).label('total_gasto')
                    )
                    .join(Venda, Cliente.cli_id == Venda.ven_cli_id)
                    .filter(Venda.ven_data.between(data_inicio, data_fim))  # Filtra pelo intervalo de datas
                    .group_by(Cliente.cli_id)
                    .order_by(desc('quantidade_compras')))  # Ordena pelo número de compras
            # Query MySQL equivalente:
            """
            SELECT cli_nome, 
                   COUNT(ven_id) AS quantidade_compras, 
                   SUM(ven_total) AS total_gasto
            FROM tb_clientes
            JOIN tb_vendas ON cli_id = ven_cli_id
            WHERE (ven_data BETWEEN ? AND ?) AND (cli_id = ? OR cli_email = ?)
            GROUP BY cli_id
            ORDER BY quantidade_compras DESC;
            """


            clientes = cliente_query.all()
            print('--------')
            print(clientes)
            return render_template('relatorios/totalcompras.html',clientes=clientes )
        except Exception as e:
            print(f"Erro ao gerar relatório de total de compras por cliente: {str(e)}")
            flash(f"Erro ao gerar relatório de total de compras por cliente: {str(e)}", "error")

    return render_template("relatorios/totalcompras.html")


@relatorio_bp.route('/compras1k', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def compras1k():
    clientes = []
    if request.method == 'POST':
        data_inicio = request.form.get("data_inicio")
        data_fim = request.form.get("data_fim")

        try:
            # Consulta para encontrar clientes com compras acima de 1000 reais no período selecionado
            clientes_query = (
                session.query(Cliente.cli_nome, Venda.ven_data, func.sum(Venda.ven_total).label('total_gasto'))
                .join(Venda, Cliente.cli_id == Venda.ven_cli_id)
                .filter(Venda.ven_data.between(data_inicio, data_fim))  # Filtra pelo intervalo de datas
                .group_by(Venda.ven_id) 
                .having(func.sum(Venda.ven_total) > 1000)  # Apenas clientes com compras acima de R$1000,00
                .order_by(desc('total_gasto'))
            )

            # Query MySQL equivalente:
            """
            SELECT cli_nome, SUM(ven_total) AS total_gasto FROM tb_clientes
            JOIN tb_vendas ON cli_id = ven_cli_id
            WHERE ven_data BETWEEN ? AND ?
            GROUP BY cli_id
            HAVING total_gasto > 1000
            ORDER BY total_gasto DESC;
            """

            clientes = clientes_query.all()

        except Exception as e:
            print(f"Erro ao gerar relatório de compras acima de 1000: {str(e)}")
            flash(f"Erro ao gerar relatório de compras acima de 1000: {str(e)}", "error")

    return render_template("relatorios/compras1k.html", clientes=clientes)


@relatorio_bp.route('/top10produtos', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def top10produtos():
    dias = request.form.get("dias", type=int, default=7)  # Pega o número de dias selecionado no formulário
    try:
        # Subquery para contar o total de produtos vendidos nos últimos X dias
        subquery = (
            session.query(VendaProdutos.vpr_pro_id, func.sum(VendaProdutos.vpr_quantproduto).label('total_vendido'))
            .join(Venda, VendaProdutos.vpr_ven_id == Venda.ven_id)
            .filter(Venda.ven_data >= func.date('now', f'-{dias} days'))  # Filtra pela data de venda
            .group_by(VendaProdutos.vpr_pro_id)
            .subquery()
        )

        # Consulta principal para pegar os 10 produtos mais vendidos
        top_produtos_query = (
            session.query(Produto.pro_nome, Produto.pro_preco, Produto.pro_estoque, subquery.c.total_vendido)
            .join(subquery, Produto.pro_nome == subquery.c.vpr_pro_id)
            .order_by(subquery.c.total_vendido.desc())
            .limit(10)
        )

        #query em mysql
        """SELECT pro_nome, SUM(vpr_quantproduto) AS total_vendido FROM tb_produtos JOIN tb_vendas_produtos 
        ON pro_id = vpr_pro_id
        JOIN tb_vendas 
        ON vpr_ven_id = ven_id
        WHERE ven_data >= CURDATE() - INTERVAL ? DAY
        GROUP BY pro_id
        ORDER BY total_vendido DESC
        LIMIT 10;"""

        # Executar a consulta
        top_produtos = top_produtos_query.all()

        print(f"Top 10 produtos mais vendidos nos últimos {dias} dias:", top_produtos)

    except Exception as e:
        print(f"Erro ao gerar relatório de top 10 produtos: {str(e)}", "error")
        flash(f"Erro ao gerar relatório de top 10 produtos: {str(e)}", "error")
        top_produtos = []

    return render_template("relatorios/top10produtos.html", produtos=top_produtos, dias=dias)


@relatorio_bp.route('/naovendidos', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def naovendidos():
    consulta = []
    dias = request.form.get("dias", type=int, default=7)
    result = []
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


        # Subquery explícita
        subquery = (
            session.query(VendaProdutos.vpr_pro_id)
            .join(Venda, VendaProdutos.vpr_ven_id == Venda.ven_id)
            .filter(Venda.ven_data >= func.date('now', f'-{dias} days'))  # Usar função compatível com SQLite
            .subquery()
        )

        # Query principal
        query = (
            session.query(Produto.pro_nome, Produto.pro_preco, Produto.pro_estoque)
            .filter(Produto.pro_nome.not_in(select(subquery)))  # Força o uso de SELECT
        )

        # Executar a consulta
        result = query.all()
        print("Resultado da consulta:", result)

    except Exception as e:
        print(f"Erro ao gerar relatório: {str(e)}", "error")
        flash(f"Erro ao gerar relatório: {str(e)}", "error")
    finally:
        return render_template("relatorios/naovendidos.html", produtos=result)
    
@relatorio_bp.route('/logs', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def logs():
    logs = LogVenda.all()
    return render_template('relatorios/logs.html', logs = logs)