from flask import Blueprint, redirect, url_for, request, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user

from models.clientes import Cliente

from database.config import session

from sqlalchemy import text

from decorators.role import role_required

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Cliente.find(id=user_id)

cliente_bp = Blueprint(name='cliente', import_name=__name__, template_folder='templates', url_prefix='/clientes')

@cliente_bp.route('/', methods=['POST', 'GET'])
@login_required
@role_required('admin')
def view():
    if request.method == 'POST':
        ordem = request.form['ordem']
        clientes = Cliente.all(ordem=ordem)
    elif request.method == 'GET':
        clientes = Cliente.all()
    return render_template('clientes/view.html', clientes = clientes)

@cliente_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha = generate_password_hash(senha)
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        telefone = str(telefone)
        tipo = 'comum'
        user = Cliente.find(email=email)
        if user:
            flash("usuário já cadastrado!", "error")
            return render_template('clientes/register.html')
        else:
            user = Cliente(cli_nome = nome, cli_email = email, cli_telefone = telefone, cli_endereco = endereco, cli_senha = senha, cli_tipo=tipo)
            session.add(user)
            session.commit()
            flash("Cliente cadastrado com Sucesso", "success")
            return redirect(url_for('produtos.view'))
    return render_template('clientes/register.html') 


@cliente_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = Cliente.find(email=email)
        if user:
            if email == user.cli_email and check_password_hash(user.cli_senha,senha):
                try:
                    login_user(user)
                    return redirect(url_for('produtos.view'))
                except:
                    flash("algo deu errado no seu login, tente novamente", "danger")
            else:
                flash("algo deu errado no seu login, tente novamente", "danger")
        else:
            flash("Usuário não cadastrado", "danger")                    
            return redirect(url_for('cliente.register'))

    return render_template('clientes/login.html') 

@cliente_bp.route('/logout', methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    flash("logout efetuado com sucesso!", "success")
    return redirect(url_for('index'))

@cliente_bp.route('/remove/<int:cli_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def remove(cli_id):
    cliente = Cliente.find(id=cli_id)
    try:
        # sql = text(f"DELETE * FROM tb_clientes WHERE cli_id = {cliente.cli_id}")
        # session.execute(sql) POR ALGUM MOTIVO NÃO TA FUNCIONANDO AAAA
        session.delete(cliente) #DELETE * FROM tb_clientes WHERE cli_id = cliente.cli_id
        session.commit()
        flash("usuário removido!", "success")
    except:
        flash("erro ao remover, tente novamente", "error")

    return redirect(url_for('cliente.view'))
    

@cliente_bp.route('/edit/<int:cli_id>', methods=['POST','GET'])
@login_required
@role_required('admin')
def edit(cli_id):
    cliente = Cliente.find(id=cli_id)
    if request.method == 'POST':
        if cliente:
            cliente.cli_nome = request.form['nome']
            cliente.cli_email = request.form['email']
            cliente.cli_telefone = str(request.form['telefone'])
            cliente.cli_endereco = request.form['endereco']

            
            try:
                session.commit() 
                flash("Edição realizada com sucesso!", "success")
            except: #se não conseguir dar o commit
                # session.rollback()  # reverte as alterações em caso de erro
                flash("Algo deu errado ao salvar as alterações, tente novamente.", "error")
        else:
            flash("Cliente não encontrado.", "error")
        
        return redirect(url_for('cliente.view'))  # Redireciona para a página de listagem

    # Se for uma requisição GET, renderiza o formulário com os dados do cliente
    if cliente:
        return render_template('clientes/edit.html', cliente=cliente)
    else:
        flash("Cliente não encontrado.", "error")
        return redirect(url_for('cliente.view'))