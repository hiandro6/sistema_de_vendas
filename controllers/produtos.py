from flask import Blueprint, redirect, url_for, request, render_template
from database.config import session
from models.produtos import Produto

produto_bp = Blueprint(name='produto', import_name=__name__, template_folder='templates', url_prefix='/produto')

# NOME PARA A PÁGINA PRINCIPAL DOS PRODUTOS, QUE LISTA OS DISPONIVEIS: /produtos/listar.html
#Nome dos produtos que tão sendo passados para a página de listar: {{produtos}} (linha 15)
#Nome dos formulário pra adcionar produtos: (Linhas 22 até 25)

@produto_bp.route('/listar')
def listar():
    if request.method == 'POST':
        ordem = request.form['ordem']
        produtos = Produto.all(ordem=ordem)
    elif request.method == 'GET':
        produtos = Produto.all()
    return render_template('clientes/index.html', produtos = produtos)

@produto_bp.route('/adicionar', methods=['POST','GET'])
def adicionar():
    if request.method == 'POST':
        nome_produto = request.form['nome'] 
        desc_produto = request.form['descricao']
        preco_produto = request.form['preco']
        estoque_produto = request.form['estoque']
        novo_produto = Produto(pro_nome = nome_produto, pro_descricao = desc_produto, pro_preco = preco_produto, pro_estoque = estoque_produto)
        session.add(novo_produto)
        session.commit()
    
    else:
        pass #Aqui vai ser o return render_template    

