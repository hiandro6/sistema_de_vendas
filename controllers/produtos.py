from flask import Blueprint, redirect, url_for, request, render_template, flash
from database.config import session
from models.produtos import Produto
from sqlalchemy import text
from flask_login import login_required

produto_bp = Blueprint(name='produtos', import_name=__name__, template_folder='templates', url_prefix='/produtos')

#Nome dos produtos que tão sendo passados para a página view: {{produtos}} (linha 17)
#Nome dos formulário pra adcionar produtos: (Linhas 22 até 25)

@produto_bp.route('/', methods=['GET','POST'])
@login_required
def view():
    if request.method == 'POST':
        ordem = request.form['ordem']
        produtos = Produto.all(ordem=ordem)
    elif request.method == 'GET':
        produtos = Produto.all()
    return render_template('produtos/view.html', produtos = produtos)

@produto_bp.route('/add', methods=['GET','POST'])
@login_required
def add():
    if request.method == 'POST':
        nome_produto = request.form['nome'] 
        desc_produto = request.form['descricao']
        preco_produto = request.form['preco']
        estoque_produto = request.form['estoque']
        if float(preco_produto) < 0:
            flash('Valor inválido','error')
            return redirect(url_for('produtos.add'))
        if float(estoque_produto) < 0:
            flash('Valor inválido','error')
            return redirect(url_for('produtos.add'))
        novo_produto = Produto(pro_nome = nome_produto, pro_descricao = desc_produto, pro_preco = preco_produto, pro_estoque = estoque_produto)
        session.add(novo_produto)
        session.commit()
        #Adcionar flash()

    
    return render_template('produtos/add.html') 
        
    
@produto_bp.route('/edit/<int:pro_id>', methods=['GET','POST'])
@login_required
def edit(pro_id):
    produto = Produto.find(id=pro_id)
    if request.method == 'POST':
        nome_produto = request.form['nome'] 
        desc_produto = request.form['descricao']
        preco_produto = request.form['preco']
        estoque_produto = request.form['estoque']
        if int(estoque_produto) < 0:
            flash('Valor inválido','error')
            return redirect(url_for('produtos.edit',pro_id=pro_id))
        if produto:
            produto.pro_nome = nome_produto
            produto.pro_descricao = desc_produto
            produto.pro_preco = preco_produto
            produto.pro_estoque = estoque_produto
            session.commit()
            #flash edição realizada com sucesso
        else:
            #Adcionar flash() de erro
            pass
        return redirect(url_for('produtos.view')) 
    else:
        return render_template('produtos/edit.html', produto=produto)

@produto_bp.route('/remove/<int:pro_id>', methods=['POST','GET'])
@login_required
def remove(pro_id):
    produto = Produto.find(id=pro_id)
    if produto:
        # session.delete(produto)
        sql = text(f"DELETE FROM tb_produtos WHERE pro_id = {produto.pro_id}")
        session.execute(sql)
        session.commit()
        flash('produto deletado')
    return redirect(url_for('produtos.view'))