from flask import Blueprint, redirect, url_for, request, render_template
from models.vendas import Venda
from models.clientes import Cliente
from models.produtos import Produto
from models.vendasprodutos import VendaProdutos
from sqlalchemy import text
from database.config import session

relatorios_bp = Blueprint(name='relatorio', import_name=__name__, template_folder='templates', url_prefix='/relatorios')

relatorios_bp.route('/')
def filtrar(filtro):
    pass
