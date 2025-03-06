from flask import Flask, render_template, url_for, redirect
from flask_login import current_user
from database import engine
from database import Base
from controllers.clientes import login_manager, cliente_bp
from controllers.produtos import produto_bp
from controllers.vendas import venda_bp
from controllers.relatorios import relatorio_bp
from database import session
from models.clientes import Cliente
from werkzeug.security import generate_password_hash
# from models.produtos import Produtos
# from models.vendas import Vendas
# from models.vendasprodutos import VendasProdutos
from models.logvenda import LogVenda

def add_admin():
    admin_existente = session.query(Cliente).filter(Cliente.cli_email == "admin@admin").first()
    print(admin_existente)
    if not admin_existente:
        user = Cliente(cli_nome = "admin", cli_email = "admin@admin", cli_telefone = "00000000", cli_endereco = "Sistema", cli_senha = generate_password_hash("123"), cli_tipo="admin")
        session.add(user)
        session.commit()
    else:
        pass

app = Flask(__name__)


app.config['SECRET_KEY'] = 'hashdhfiogoq3812021fsa'


login_manager.init_app(app)

with app.app_context():
    Base.metadata.create_all(bind=engine)


app.register_blueprint(cliente_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(venda_bp)
app.register_blueprint(relatorio_bp)

@app.route('/')
def index():
    add_admin()
    if current_user.is_authenticated:
        return redirect(url_for('produtos.view'))
    return render_template('index.html')

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('cliente.login'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404