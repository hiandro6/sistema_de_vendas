from flask import Blueprint, redirect, url_for, request, render_template

from flask_login import LoginManager, login_required, login_user, logout_user

from models.clientes import Clientes

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Clientes.find(cli_id=user_id)

auth_bp = Blueprint(
    name='auth',
    import_name=__name__,
    template_folder='templates')

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']

        user = Clientes.find(email=email)
        if user:
            login_user(user)
            return redirect(url_for('users.index'))
        
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))