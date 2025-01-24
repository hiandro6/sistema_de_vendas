from flask import Blueprint, redirect, url_for, request, render_template

from flask_login import LoginManager, login_required, login_user, logout_user

from models.clientes import Cliente

from database.config import session

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Cliente.find(cli_id=user_id)

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
            #exibir mensagem de usuário já cadastrado
            return redirect(url_for('login')) 
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
            if nome == user.nome and email == user.email:
                login_user(user)
                return redirect(url_for('view')) 
    else:
        return render_template('clientes/login.html') 

@cliente_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    #talvez colocar flash message logout efetuado com sucesso
    return redirect(url_for('view'))

@cliente_bp.route('/remove/<int:cli_id>', methods=['POST'])
def remove(cli_id):
    cliente = Cliente.find(id=cli_id)
    session.delete(cliente)
    session.commit()
    return redirect(url_for('view'))
    #ADCIONAR FLASH()

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
            #flash operação realizada com sucesso
        else:
            #Adcionar flash() de erro
            pass
    else:
        render_template('clientes/edit.html')
    return redirect(url_for('view'))
