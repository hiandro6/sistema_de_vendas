from flask import Flask, render_template
from database.config import engine
from database import Base
from controllers.clientes import login_manager, cliente_bp
from controllers.produtos import produto_bp
from controllers.vendas import venda_bp
# from models.clientes import Clientes
# from models.produtos import Produtos
# from models.vendas import Vendas
# from models.vendasprodutos import VendasProdutos


app = Flask(__name__)


app.config['SECRET_KEY'] = 'hashdhfiogoq3812021fsa'


login_manager.init_app(app)

with app.app_context():
    Base.metadata.create_all(bind=engine)


app.register_blueprint(cliente_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(venda_bp)

@app.route('/')
def index():
    return render_template('index.html')

