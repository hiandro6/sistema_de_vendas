from flask import Blueprint, redirect, url_for, request, render_template
from models.vendas import Venda
from models.clientes import Cliente
from models.produtos import Produto
from models.vendasprodutos import VendaProdutos

from database.config import session


venda_bp = Blueprint(name='venda', import_name=__name__, template_folder='templates')

@venda_bp.route('/view', methods=['POST', 'GET'])
def view():
    if request.method == 'POST':
        ordem = request.form['ordem']
        vendas = Venda.all(ordem=ordem)
    elif request.method == 'GET':
        vendas = Venda.all()
    return render_template('vendas/view.html', vendas = vendas)

@venda_bp.route('/nova_venda', methods=['POST', 'GET'])
def nova_venda():
    if request.method == 'POST':
        data = request.form['data']
        produtos = request.form.getlist('produtos')
        quantidades = request.form.getlist('quantidades')

        info_cliente = request.form['id_cliente']
        if info_cliente.isnumeric(): #se o dado for um número fazemos a busca por id, caso contrário buscamos pelo email
            cliente = Cliente.find(id = info_cliente)
        else:
            cliente = Cliente.find(email = info_cliente)

        total = 0
        for i in range (0, len(produtos)): #calculando o valor total da venda e diminuindo as quantidades do estoque
            preco = session.execute("SELECT pro_preco FROM tb_produtos WHERE pro_nome = :nome", {"nome": produtos[i]}).scalar()
            total += preco * int(quantidades[i])
            
            estoque_atual = Produto.estoque(nome = produtos[i])
            novo_estoque = estoque_atual - int(quantidades[i]) 
            session.execute("UPDATE tb_produtos SET pro_estoque = :quantidade WHERE pro_nome = :nome", {"quantidade": novo_estoque, "nome": produtos[i]})


        venda = Venda(ven_data=data, ven_cli_id=cliente.cli_id, ven_total=total) #criando a venda
        session.add(venda)
        session.commit()


        #adicionando os produtos vendidos
        for i in range(len(produtos)):
            preco_result = session.execute("SELECT pro_preco FROM tb_produtos WHERE pro_nome = :nome", {"nome": produtos[i]})
            preco = preco_result.scalar()
            quantidade = int(quantidades[i])
            venda_produto = VendaProdutos(vpr_ven_id=venda.ven_id, vpr_pro_id=produtos[i], vpr_quantidade=quantidade, vpr_preco_unitario=preco)
            session.add(venda_produto)
            session.commit()

        return redirect(url_for('venda.view'))
    else: 
        render_template('vendas/nova_venda.html')