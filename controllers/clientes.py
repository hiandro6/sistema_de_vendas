from flask import Blueprint, redirect, url_for, request, render_template, flash

from flask_login import LoginManager, login_required, login_user, logout_user

from models.clientes import Cliente

from database.config import session

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Cliente.find(id=user_id)

cliente_bp = Blueprint(name='cliente', import_name=__name__, template_folder='templates', url_prefix='/clientes')

@cliente_bp.route('/view', methods=['POST', 'GET'])
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
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        user = Cliente.find(email=email)
        if user:
            flash("usuário já cadastrado!", "warning")
            return redirect(url_for('cliente.login')) 
        else:
            user = Cliente(cli_nome = nome, cli_email = email, cli_telefone = telefone, cli_endereco = endereco)
            session.add(user)
            session.commit()
    return render_template('clientes/register.html') 


@cliente_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        user = Cliente.find(email=email)
        if user:
            if nome == user.cli_nome and email == user.cli_email:
                try:
                    login_user(user)
                    return redirect(url_for('cliente.view'))
                except:
                    flash("algo deu errado no seu login, tente novamente", "error")
    return render_template('clientes/login.html') 

@cliente_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("logout efetuado com sucesso!", "success")
    return redirect(url_for('cliente.view'))

@cliente_bp.route('/remove/<int:cli_id>', methods=['POST'])
def remove(cli_id):
    cliente = Cliente.find(id=cli_id)
    session.delete(cliente)
    session.commit()
    flash("usuário removido!", "success")
    return redirect(url_for('cliente.view'))
    

@cliente_bp.route('/edit/<int:cli_id>', methods=['POST','GET'])
def edit(cli_id):
    if request.method == 'POST':
        nome_cliente = request.form['nome'] 
        email_cliente = request.form['email']
        telefone_cliente = request.form['telefone']
        endereco_cliente = request.form['endereco']
        cliente = cliente.find(id=cli_id)
        if cliente:
            cliente.cli_nome = nome_cliente
            cliente.cli_email = email_cliente
            cliente.cli_telefone = telefone_cliente
            cliente.cli_endereco = endereco_cliente
            session.commit()
            flash("edição realizada!", "success")
        else:
            flash("algo deu errado ao editar, tente novamente", "error")
    else:
        return render_template('clientes/edit.html')
    
    return redirect(url_for('cliente.view'))
