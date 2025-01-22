from flask import Flask
from database.config import start_db
from models import clientes, vendas, produtos, vendasprodutos, produtos
from database.config import session
from controllers.clientes import login_manager, cliente_bp
from controllers.produtos import produto_bp
from controllers.vendas import venda_bp


app = Flask(__name__)


app.config['SECRET_KEY'] = 'hashdhfiogoq3812021fsa'


login_manager.init_app(app)


app.register_blueprint(cliente_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(venda_bp)

@app.route('/')
def index():
    return "<h1>Teste</h1>"
start_db()

