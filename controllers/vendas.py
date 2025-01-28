from flask import Blueprint, redirect, url_for, request, render_template, flash
from models.vendas import Venda
from models.clientes import Cliente
from models.produtos import Produto
from models.vendasprodutos import VendaProdutos
from sqlalchemy import text
from database.config import session


venda_bp = Blueprint(name='venda', import_name=__name__, template_folder='templates', url_prefix='/vendas')

@venda_bp.route('/', methods=['POST', 'GET'])
def view():
    if request.method == 'POST':
        ordem = request.form['ordem']
        vendas = Venda.all(ordem=ordem)
    elif request.method == 'GET':
        sql = text(f"SELECT * FROM tb_vendas JOIN tb_clientes ON ven_cli_id = cli_id")
        # vendas = Venda.all()
        # vendapro = VendaProdutos.find(ven_id = vendas)
        vendas = session.execute(sql)
    return render_template('vendas/view.html', vendas = vendas)

@venda_bp.route('/nova_venda', methods=['POST', 'GET'])
def nova_venda():
    if request.method == 'POST':
        data = request.form['data']
        produtos = request.form.getlist('produtos')
        quantidades = request.form.getlist('quantidades')

        info_cliente = request.form['id_cliente']
        if info_cliente.isnumeric(): #se o dado for um número fazemos a busca por id, caso contrário buscamos pelo email
            cliente = Cliente.find(id = info_cliente)
        else:
            cliente = Cliente.find(email = info_cliente)

        total = 0
        for i in range (0, len(produtos)): #calculando o valor total da venda e diminuindo as quantidades do estoque
            preco_sql = text("SELECT pro_preco FROM tb_produtos WHERE pro_nome = :nome")
            preco = session.execute(preco_sql, {"nome": produtos[i]}).scalar()
            if preco is None:
                return f"Erro: O produto '{produtos[i]}' não foi encontrado no banco de dados.", 400
            preco = float(preco)

            total += preco * int(quantidades[i])
            
            update_sql = text("UPDATE tb_produtos SET pro_estoque = :quantidade WHERE pro_nome = :nome")
            estoque_atual = Produto.estoque(nome = produtos[i])
            novo_estoque = estoque_atual - int(quantidades[i]) 
            if novo_estoque < 0:
                return f"Erro: Estoque insuficiente para o produto '{produtos[i]}'.", 400

            session.execute(update_sql, {"quantidade": novo_estoque, "nome": produtos[i]})

        try:
            venda = Venda(ven_data=data, ven_cli_id=cliente.cli_id, ven_total=total) #criando a venda
            session.add(venda)
            session.commit()
        except:
            flash("ocorreu um erro ao cadastrar a venda", "error")
            return redirect(url_for('venda.nova_venda'))


        #adicionando os produtos vendidos
        for i in range(len(produtos)):
            sql = text("SELECT pro_preco FROM tb_produtos WHERE pro_nome = :nome")
            preco_result = session.execute(sql, {"nome": produtos[i]})
            preco = preco_result.scalar()
            quantidade = int(quantidades[i])
            venda_produto = VendaProdutos(vpr_ven_id=venda.ven_id, vpr_pro_id=produtos[i], vpr_quantproduto=quantidade, vpr_precoproduto=preco)
            session.add(venda_produto)
            session.commit()

        return redirect(url_for('venda.view'))
    else: 
        return render_template('vendas/nova_venda.html', produtos = Produto.all())
    

@venda_bp.route('/edit/<int:venda_id>', methods=['POST', 'GET'])
def edit(venda_id):
    if request.method == 'POST':
        # Coletar dados do formulário
        data = request.form['data']
        produtos = request.form.getlist('produtos')
        quantidades = request.form.getlist('quantidades')

        # Buscar a venda existente
        venda_sql = text("SELECT * FROM tb_vendas WHERE ven_id = :venda_id")
        venda = session.execute(venda_sql, {"venda_id": venda_id}).fetchone()

        if not venda:
            return f"Erro: Venda com ID {venda_id} não encontrada.", 404

        # Atualizar a venda
        update_venda_sql = text("UPDATE tb_vendas SET ven_data = :data WHERE ven_id = :venda_id")
        session.execute(update_venda_sql, {"data": data, "venda_id": venda_id})

        # Deletar produtos relacionados à venda
        delete_venda_produtos_sql = text("DELETE FROM tb_vendas_produtos WHERE vpr_ven_id = :venda_id")
        session.execute(delete_venda_produtos_sql, {"venda_id": venda_id})

        # Inicializar o total da venda
        total = 0

        # Adicionar os novos produtos da venda
        for i in range(len(produtos)):
            # Atualizar estoque do produto
            produto_nome = produtos[i]
            quantidade = int(quantidades[i])

            estoque_atual_sql = text("SELECT pro_estoque FROM tb_produtos WHERE pro_nome = :produto_nome")
            estoque_atual = session.execute(estoque_atual_sql, {"produto_nome": produto_nome}).scalar()

            if estoque_atual < quantidade:
                return f"Erro: Estoque insuficiente para o produto '{produto_nome}'.", 400

            novo_estoque = estoque_atual - quantidade
            update_estoque_sql = text("UPDATE tb_produtos SET pro_estoque = :novo_estoque WHERE pro_nome = :produto_nome")
            session.execute(update_estoque_sql, {"novo_estoque": novo_estoque, "produto_nome": produto_nome})

            # Obter o preço do produto
            preco_sql = text("SELECT pro_preco FROM tb_produtos WHERE pro_nome = :produto_nome")
            preco = session.execute(preco_sql, {"produto_nome": produto_nome}).scalar()

            # Calcular o total da venda
            total += preco * quantidade

            # Inserir o novo produto na venda
            insert_venda_produtos_sql = text("""
                INSERT INTO tb_vendas_produtos (vpr_ven_id, vpr_pro_id, vpr_quantproduto, vpr_precoproduto)
                VALUES (:venda_id, :produto_nome, :quantidade, :preco)
            """)
            session.execute(insert_venda_produtos_sql, {
                "venda_id": venda_id,
                "produto_nome": produto_nome,
                "quantidade": quantidade,
                "preco": preco
            })

        # Atualizar o valor total da venda na tabela `tb_vendas`
        update_total_sql = text("UPDATE tb_vendas SET ven_total = :total WHERE ven_id = :venda_id")
        session.execute(update_total_sql, {"total": total, "venda_id": venda_id})

        # Confirmar as alterações
        session.commit()

        return redirect(url_for('venda.view'))

    else:
        # Buscar os dados da venda para exibir no formulário
        venda_sql = text("SELECT * FROM tb_vendas WHERE ven_id = :venda_id")
        venda = session.execute(venda_sql, {"venda_id": venda_id}).fetchone()

        if not venda:
            return f"Erro: Venda com ID {venda_id} não encontrada.", 404

        venda_produtos_sql = text("""
            SELECT vp.vpr_quantproduto, p.pro_nome 
            FROM tb_vendas_produtos vp
            JOIN tb_produtos p ON vp.vpr_pro_id = p.pro_nome
            WHERE vp.vpr_ven_id = :venda_id
        """)
        venda_produtos = session.execute(venda_produtos_sql, {"venda_id": venda_id}).fetchall()

        return render_template('vendas/edit.html', venda=venda, venda_produtos=venda_produtos, produtos=Produto.all())

@venda_bp.route('/remove/<int:venda_id>', methods=['POST', 'GET'])
def remove(venda_id):
    print('ENTROU NA ROTA')
    # Buscar a venda para verificar se existe
    venda_sql = text("SELECT * FROM tb_vendas WHERE ven_id = :venda_id")
    venda = session.execute(venda_sql, {"venda_id": venda_id}).fetchone()
    # venda = Venda.find(id = venda_id)
    venda_produto = VendaProdutos.find(vpr_id = venda_id)
    if not venda:
        return f"Erro: Venda com ID {venda_id} não encontrada.", 404

    try:
        # Buscar os produtos associados à venda
        venda_produtos_sql = text("""
            SELECT vpr_pro_id, vpr_quantproduto
            FROM tb_vendas_produtos
            WHERE vpr_ven_id = :venda_id
        """)
        print('vai pegar venda_produtos')
        venda_produtos = session.execute(venda_produtos_sql, {"venda_id": venda_id}).fetchall()
        print('pegou quem é venda_produtos')

        # Restaurar o estoque dos produtos
        for produto in venda_produtos:
            produto_nome = produto[0]  # Aqui o nome do produto está armazenado em vpr_pro_id
            quantidade_vendida = produto[1]  # vpr_quantproduto
            
            print(f"Produto Nome: {produto_nome}")
            
            # Buscar o ID e o estoque do produto com base no nome
            produto_info_sql = text("SELECT pro_id, pro_estoque FROM tb_produtos WHERE pro_nome = :produto_nome")
            produto_info = session.execute(produto_info_sql, {"produto_nome": produto_nome}).fetchone()

            if not produto_info:
                print(f"Erro: Produto '{produto_nome}' não encontrado na tabela 'tb_produtos'.")
                continue
            
            produto_id = produto_info.pro_id
            estoque_atual = produto_info.pro_estoque

            print(f"Produto ID: {produto_id}, Estoque Atual: {estoque_atual}, Quantidade Vendida: {quantidade_vendida}")

            # Atualizar o estoque do produto
            novo_estoque = estoque_atual + quantidade_vendida
            update_estoque_sql = text("UPDATE tb_produtos SET pro_estoque = :novo_estoque WHERE pro_id = :produto_id")
            session.execute(update_estoque_sql, {"novo_estoque": novo_estoque, "produto_id": produto_id})
            print(f"Estoque atualizado para o produto '{produto_nome}' (ID: {produto_id}).")
            session.commit()


        # Deletar os produtos associados à venda
        delete_venda_produtos_sql = text("DELETE FROM tb_vendas_produtos WHERE vpr_ven_id = :venda_id")
        session.execute(delete_venda_produtos_sql, {"venda_id": venda_id})
        print('DELETOU A VENDA PRODUTOS')

        # Deletar a venda
        delete_venda_sql = text("DELETE FROM tb_vendas WHERE ven_id = :venda_id")
        session.execute(delete_venda_sql, {"venda_id": venda_id})
        print('DELETOU A VENDA')

        # Confirmar as alterações no banco de dados
        session.commit()

        flash("Venda removida com sucesso!", "success")
        return redirect(url_for('venda.view'))

    except Exception as e:
        session.rollback()
        print(f"Erro ao remover a venda: {e}")
        flash(f"Erro ao remover a venda: {str(e)}", "error")
        return redirect(url_for('venda.view'))
