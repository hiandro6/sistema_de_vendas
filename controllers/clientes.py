from flask import Blueprint, redirect, url_for, request, render_template

from flask_login import LoginManager, login_required, login_user, logout_user

from models.clientes import Clientes

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Clientes.find(cli_id=user_id)

cliente_bp = Blueprint(name='cliente', import_name=__name__, template_folder='templates')

@cliente_bp.route('/login', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        endereco = request.form['endereco']
        user = Clientes.find(email=email)
        if user:
            #exibir mensagem de usuário já cadastrado
            return redirect(url_for('login')) 
        
    return render_template('cliente/login.html') 


@cliente_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']

        user = Clientes.find(email=email)
        if user:
            login_user(user)
            return redirect(url_for('index')) 
        
    return render_template('cliente/login.html') 

@cliente_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))