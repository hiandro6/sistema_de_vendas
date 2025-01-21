from flask import Flask
from database.config import start_db
from models import clientes, vendas, produtos, vendasprodutos, produtos
from database.config import session


app = Flask(__name__)

# configurar secret key (PROVA)
app.config['SECRET_KEY'] = 'ALOHA'

# inicializar o app no login manager (PROVA)
login_manager.init_app(app)

# registrando o blueprint (PROVA)
app.register_blueprint(auth_bp)

app.register_blueprint(users.bp)
app.register_blueprint(books.bp)

@app.route('/')
def index():
    return "<h1>Teste</h1>"
start_db()

