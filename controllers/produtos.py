from flask import Blueprint, redirect, url_for, request, render_template, flash
from database.config import session
from models.produtos import Produto

produto_bp = Blueprint(name='produto', import_name=__name__, template_folder='templates', url_prefix='/produto')

#Nome dos produtos que tão sendo passados para a página view: {{produtos}} (linha 17)
#Nome dos formulário pra adcionar produtos: (Linhas 22 até 25)

@produto_bp.route('/view', methods=['GET','POST'])
def view():
    if request.method == 'POST':
        ordem = request.form['ordem']
        produtos = Produto.all(ordem=ordem)
    elif request.method == 'GET':
        produtos = Produto.all()
    return render_template('produtos/view.html', produtos = produtos)

@produto_bp.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        nome_produto = request.form['nome'] 
        desc_produto = request.form['descricao']
        preco_produto = request.form['preco']
        estoque_produto = request.form['estoque']
        novo_produto = Produto(pro_nome = nome_produto, pro_descricao = desc_produto, pro_preco = preco_produto, pro_estoque = estoque_produto)
        session.add(novo_produto)
        session.commit()
        #Adcionar flash()
    else:
        return render_template('produtos/add.html') 
        
    
@produto_bp.route('/edit/<int:pro_id>', methods=['GET','POST'])
def edit(pro_id):
    produto = Produto.find(id=pro_id)
    if produto:
        return render_template('produtos/edit.html')
    else:
        #Adcionar flash() de erro
        pass
    return redirect(url_for('view')) #TALVEZ TENHA UM ERRO AQUI, não lembro se era pra ser produto.view

@produto_bp.route('/remove/<int:pro_id>', methods=['POST'])
def remove(pro_id):
    produto = Produto.find(id=pro_id)
    if produto:
        session.delete(produto)
        session.commit()
        #adcionar flash() confirmando o delete
    return redirect(url_for('view')) #TALVEZ TENHA UM ERRO AQUI, não lembro se era pra ser produto.view