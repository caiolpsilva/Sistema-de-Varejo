import sys
from zodb_model import ZODBHandler, Product
from mongodb_handler import MongoDBHandler
from sql_handler import MySQLHandler
from temporal_analysis import TemporalAnalysis
import pandas as pd

def print_main_menu():
    print("=== SISTEMA DE GERENCIAMENTO DE PRODUTOS ===")
    print("1. Gestão de Produtos")
    print("2. Controle de Estoque")
    print("3. Histórico de Preços")
    print("4. Vendas")
    print("5. Promoções")
    print("6. Avaliações de Clientes")
    print("7. Relatórios")
    print("0. Sair")

def print_product_management_menu():
    print("\n--- Gestão de Produtos ---")
    print("1. Listar todos os produtos")
    print("2. Buscar produto por ID ou nome")
    print("3. Adicionar novo produto")
    print("4. Atualizar produto")
    print("5. Remover produto")
    print("0. Voltar ao menu principal")

def list_all_products(sql_handler):
    query = """
    SELECT p.id_produto, p.codigo_produto, p.nome_produto, c.nome_categoria, p.preco_atual, p.unidade_medida
    FROM produto p
    LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
    ORDER BY p.id_produto
    """
    products = sql_handler.execute_query(query)
    if not products:
        print("Nenhum produto encontrado.")
        return
    print("\nID | Código     | Nome                             | Categoria           | Preço Atual | Unidade")
    print("---|------------|---------------------------------|---------------------|-------------|---------")
    for prod in products:
        print(f"{prod['id_produto']: <3}| {prod['codigo_produto']: <10}| {prod['nome_produto']: <33}| {prod['nome_categoria'] if prod['nome_categoria'] else 'N/A': <19}| R$ {prod['preco_atual']: <10.2f}| {prod['unidade_medida']}")

def search_product(sql_handler):
    search_term = input("Digite o ID ou nome do produto para buscar: ").strip()
    if search_term.isdigit():
        query = """
        SELECT p.id_produto, p.codigo_produto, p.nome_produto, c.nome_categoria, p.preco_atual, p.unidade_medida
        FROM produto p
        LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
        WHERE p.id_produto = %s
        """
        products = sql_handler.execute_query(query, (int(search_term),))
    else:
        query = """
        SELECT p.id_produto, p.codigo_produto, p.nome_produto, c.nome_categoria, p.preco_atual, p.unidade_medida
        FROM produto p
        LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
        WHERE p.nome_produto LIKE %s
        """
        products = sql_handler.execute_query(query, (f"%{search_term}%",))
    if not products:
        print("Produto não encontrado.")
        return
    print("\nID | Código     | Nome                             | Categoria           | Preço Atual | Unidade")
    print("---|------------|---------------------------------|---------------------|-------------|---------")
    for prod in products:
        print(f"{prod['id_produto']: <3}| {prod['codigo_produto']: <10}| {prod['nome_produto']: <33}| {prod['nome_categoria'] if prod['nome_categoria'] else 'N/A': <19}| R$ {prod['preco_atual']: <10.2f}| {prod['unidade_medida']}")

def add_new_product(sql_handler):
    codigo = input("Código do produto: ").strip()
    nome = input("Nome do produto: ").strip()
    categoria_id = input("ID da categoria: ").strip()
    preco = input("Preço atual: ").strip()
    unidade = input("Unidade (ex: UN, KG): ").strip()
    try:
        preco_float = float(preco)
        categoria_id_int = int(categoria_id)
    except ValueError:
        print("Preço ou ID da categoria inválidos.")
        return
    query = """
    INSERT INTO produto (codigo_produto, nome_produto, id_categoria, preco_atual, unidade_medida)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        sql_handler.execute_query(query, (codigo, nome, categoria_id_int, preco_float, unidade), commit=True)
        print("Produto adicionado com sucesso.")
    except Exception as e:
        print(f"Erro ao adicionar produto: {e}")

def update_product(sql_handler):
    product_id = input("Digite o ID do produto a ser atualizado: ").strip()
    if not product_id.isdigit():
        print("ID inválido.")
        return
    product_id_int = int(product_id)
    # Check if product exists
    query_check = "SELECT * FROM produto WHERE id_produto = %s"
    product = sql_handler.execute_query(query_check, (product_id_int,))
    if not product:
        print("Produto não encontrado.")
        return
    print("Deixe o campo vazio para não alterar o valor.")
    codigo = input("Novo código do produto: ").strip()
    nome = input("Novo nome do produto: ").strip()
    categoria_id = input("Novo ID da categoria: ").strip()
    preco = input("Novo preço atual: ").strip()
    unidade = input("Nova unidade (ex: UN, KG): ").strip()
    # Build update query dynamically
    fields = []
    values = []
    if codigo:
        fields.append("codigo_produto = %s")
        values.append(codigo)
    if nome:
        fields.append("nome_produto = %s")
        values.append(nome)
    if categoria_id:
        if not categoria_id.isdigit():
            print("ID da categoria inválido.")
            return
        fields.append("id_categoria = %s")
        values.append(int(categoria_id))
    if preco:
        try:
            preco_float = float(preco)
            fields.append("preco_atual = %s")
            values.append(preco_float)
        except ValueError:
            print("Preço inválido.")
            return
    if unidade:
        fields.append("unidade_medida = %s")
        values.append(unidade)
    if not fields:
        print("Nenhuma alteração informada.")
        return
    values.append(product_id_int)
    query_update = f"UPDATE produto SET {', '.join(fields)} WHERE id_produto = %s"
    try:
        sql_handler.execute_query(query_update, tuple(values), commit=True)
        print("Produto atualizado com sucesso.")
    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")

def remove_product(sql_handler):
    product_id = input("Digite o ID do produto a ser removido: ").strip()
    if not product_id.isdigit():
        print("ID inválido.")
        return
    product_id_int = int(product_id)
    query_check = "SELECT * FROM produto WHERE id_produto = %s"
    product = sql_handler.execute_query(query_check, (product_id_int,))
    if not product:
        print("Produto não encontrado.")
        return
    confirm = input(f"Tem certeza que deseja remover o produto ID {product_id_int}? (s/n): ").strip().lower()
    if confirm != 's':
        print("Remoção cancelada.")
        return
    query_delete = "DELETE FROM produto WHERE id_produto = %s"
    try:
        sql_handler.execute_query(query_delete, (product_id_int,), commit=True)
        print("Produto removido com sucesso.")
    except Exception as e:
        print(f"Erro ao remover produto: {e}")

def main():
    print("Iniciando Sistema de Gerenciamento de Produtos")

    # Inicializa handlers
    zodb_handler = ZODBHandler()
    mongo_handler = MongoDBHandler()
    sql_handler = MySQLHandler()

    while True:
        print_main_menu()
        choice = input("Escolha uma opção: ").strip()
        if choice == '1':
            while True:
                print_product_management_menu()
                pm_choice = input("Escolha uma opção: ").strip()
                if pm_choice == '1':
                    list_all_products(sql_handler)
                elif pm_choice == '2':
                    search_product(sql_handler)
                elif pm_choice == '3':
                    add_new_product(sql_handler)
                elif pm_choice == '4':
                    update_product(sql_handler)
                elif pm_choice == '5':
                    remove_product(sql_handler)
                elif pm_choice == '0':
                    break
                else:
                    print("Opção inválida.")
        elif choice == '2':
            def print_stock_control_menu():
                print("\n--- Controle de Estoque ---")
                print("1. Listar estoque")
                print("2. Atualizar quantidade de estoque")
                print("0. Voltar ao menu principal")

            def list_stock(sql_handler):
                query = """
                SELECT e.id_produto, p.codigo_produto, p.nome_produto, e.quantidade_atual, e.quantidade_minima, e.quantidade_maxima
                FROM estoque e
                JOIN produto p ON e.id_produto = p.id_produto
                ORDER BY e.id_produto
                """
                stock_items = sql_handler.execute_query(query)
                if not stock_items:
                    print("Nenhum item de estoque encontrado.")
                    return
                print("\nID Produto | Código Produto | Nome Produto                  | Qtde Atual | Qtde Mínima | Qtde Máxima")
                print("-----------|----------------|------------------------------|------------|-------------|------------")
                for item in stock_items:
                    print(f"{item['id_produto']: <10}| {item['codigo_produto']: <14}| {item['nome_produto']: <30}| {item['quantidade_atual']: <10}| {item['quantidade_minima']: <11}| {item['quantidade_maxima']: <11}")

            def update_stock(sql_handler):
                product_id = input("Digite o ID do produto para atualizar o estoque: ").strip()
                if not product_id.isdigit():
                    print("ID inválido.")
                    return
                product_id_int = int(product_id)
                query_check = "SELECT * FROM estoque WHERE id_produto = %s"
                stock = sql_handler.execute_query(query_check, (product_id_int,))
                if not stock:
                    print("Produto não encontrado no estoque.")
                    return
                new_quantity = input("Digite a nova quantidade atual: ").strip()
                if not new_quantity.isdigit():
                    print("Quantidade inválida.")
                    return
                new_quantity_int = int(new_quantity)
                query_update = "UPDATE estoque SET quantidade_atual = %s WHERE id_produto = %s"
                try:
                    sql_handler.execute_query(query_update, (new_quantity_int, product_id_int), commit=True)
                    print("Estoque atualizado com sucesso.")
                except Exception as e:
                    print(f"Erro ao atualizar estoque: {e}")

            while True:
                print_stock_control_menu()
                sc_choice = input("Escolha uma opção: ").strip()
                if sc_choice == '1':
                    list_stock(sql_handler)
                elif sc_choice == '2':
                    update_stock(sql_handler)
                elif sc_choice == '0':
                    break
                else:
                    print("Opção inválida.")
        elif choice == '3':
            def print_price_history_menu():
                print("\n--- Histórico e Análise Temporal ---")
                print("1. Mostrar tendência histórica de preço")
                print("2. Mostrar tendência histórica de estoque")
                print("3. Prever vendas futuras")
                print("0. Voltar ao menu principal")

            def load_sales_data(sql_handler):
                query = """
                SELECT v.data_venda as date, iv.id_produto as product_id, iv.preco_unitario as price,
                       e.quantidade_atual as stock, iv.quantidade as sales
                FROM venda v
                JOIN item_venda iv ON v.id_venda = iv.id_venda
                LEFT JOIN estoque e ON iv.id_produto = e.id_produto
                ORDER BY v.data_venda
                """
                data = sql_handler.execute_query(query)
                if not data:
                    print("Nenhum dado de vendas encontrado para análise temporal.")
                    return None
                import pandas as pd
                df = pd.DataFrame(data)
                return df

            while True:
                print_price_history_menu()
                ph_choice = input("Escolha uma opção: ").strip()
                if ph_choice in ['1', '2', '3']:
                    product_id = input("Digite o ID do produto para análise: ").strip()
                    if not product_id.isdigit():
                        print("ID inválido.")
                        continue
                    product_id_int = int(product_id)
                    sales_data = load_sales_data(sql_handler)
                    if sales_data is None:
                        continue
                    from temporal_analysis import TemporalAnalysis
                    ta = TemporalAnalysis(sales_data)
                    if ph_choice == '1':
                        ta.historical_price_trend(product_id_int)
                    elif ph_choice == '2':
                        ta.historical_stock_trend(product_id_int)
                    elif ph_choice == '3':
                        ta.forecast_sales(product_id_int)
                elif ph_choice == '0':
                    break
                else:
                    print("Opção inválida.")
        elif choice == '4':
            def print_sales_menu():
                print("\n--- Vendas ---")
                print("1. Listar vendas")
                print("0. Voltar ao menu principal")

            def list_sales(sql_handler):
                query = """
                SELECT v.id_venda, v.numero_venda, c.nome as cliente_nome, l.nome_loja, v.data_venda, v.valor_total, v.status_venda
                FROM venda v
                LEFT JOIN cliente c ON v.id_cliente = c.id_cliente
                LEFT JOIN loja l ON v.id_loja = l.id_loja
                ORDER BY v.data_venda DESC
                """
                sales = sql_handler.execute_query(query)
                if not sales:
                    print("Nenhuma venda encontrada.")
                    return
                print("\nID Venda | Número Venda | Cliente               | Loja                | Data Venda           | Valor Total | Status")
                print("---------|--------------|-----------------------|---------------------|----------------------|-------------|---------")
                for sale in sales:
                    print(f"{sale['id_venda']: <8}| {sale['numero_venda']: <12}| {sale['cliente_nome'] if sale['cliente_nome'] else 'N/A': <21}| {sale['nome_loja'] if sale['nome_loja'] else 'N/A': <20}| {sale['data_venda']} | R$ {sale['valor_total']: <10.2f}| {sale['status_venda']}")

            while True:
                print_sales_menu()
                sales_choice = input("Escolha uma opção: ").strip()
                if sales_choice == '1':
                    list_sales(sql_handler)
                elif sales_choice == '0':
                    break
                else:
                    print("Opção inválida.")
        elif choice == '5':
            def print_promotions_menu():
                print("\n--- Promoções ---")
                print("1. Listar promoções")
                print("0. Voltar ao menu principal")

            def list_promotions(sql_handler):
                query = """
                SELECT id_promocao, nome_promocao, descricao, data_inicio, data_fim, percentual_desconto
                FROM promocao
                ORDER BY data_inicio DESC
                """
                promotions = sql_handler.execute_query(query)
                if not promotions:
                    print("Nenhuma promoção encontrada.")
                    return
                print("\nID Promoção | Nome Promoção           | Descrição                      | Início      | Fim        | % Desconto")
                print("------------|-------------------------|-------------------------------|-------------|------------|------------")
                for promo in promotions:
                    print(f"{promo['id_promocao']: <11}| {promo['nome_promocao']: <23}| {promo['descricao']: <30}| {promo['data_inicio']} | {promo['data_fim']} | {promo['percentual_desconto']: <10.2f}")

            while True:
                print_promotions_menu()
                promo_choice = input("Escolha uma opção: ").strip()
                if promo_choice == '1':
                    list_promotions(sql_handler)
                elif promo_choice == '0':
                    break
                else:
                    print("Opção inválida.")
        elif choice == '6':
            def print_reviews_menu():
                print("\n--- Avaliações de Clientes ---")
                print("1. Listar avaliações de produtos")
                print("0. Voltar ao menu principal")

            def list_reviews(sql_handler):
                query = """
                SELECT a.id_avaliacao, p.nome_produto, c.nome as cliente_nome, a.data_avaliacao, a.nota, a.comentario
                FROM avaliacao a
                LEFT JOIN produto p ON a.id_produto = p.id_produto
                LEFT JOIN cliente c ON a.id_cliente = c.id_cliente
                ORDER BY a.data_avaliacao DESC
                """
                reviews = sql_handler.execute_query(query)
                if not reviews:
                    print("Nenhuma avaliação encontrada.")
                    return
                print("\nID Avaliação | Produto                      | Cliente               | Data Avaliação       | Nota | Comentário")
                print("------------|------------------------------|-----------------------|----------------------|------|-----------")
                for review in reviews:
                    print(f"{review['id_avaliacao']: <12}| {review['nome_produto'] if review['nome_produto'] else 'N/A': <28}| {review['cliente_nome'] if review['cliente_nome'] else 'N/A': <21}| {review['data_avaliacao']} | {review['nota']: <4} | {review['comentario']}")

            while True:
                print_reviews_menu()
                review_choice = input("Escolha uma opção: ").strip()
                if review_choice == '1':
                    list_reviews(sql_handler)
                elif review_choice == '0':
                    break
                else:
                    print("Opção inválida.")
        elif choice == '7':
            def print_reports_menu():
                print("\n--- Relatórios ---")
                print("1. Total de registros por tabela")
                print("2. Vendas por loja")
                print("3. Produtos mais vendidos")
                print("4. Clientes com maior volume de compras")
                print("0. Voltar ao menu principal")

            def total_records(sql_handler):
                query = """
                SELECT 'Categorias' as Tabela, COUNT(*) as Total FROM categoria
                UNION ALL
                SELECT 'Produtos', COUNT(*) FROM produto
                UNION ALL
                SELECT 'Clientes', COUNT(*) FROM cliente
                UNION ALL
                SELECT 'Lojas', COUNT(*) FROM loja
                UNION ALL
                SELECT 'Funcionários', COUNT(*) FROM funcionario
                UNION ALL
                SELECT 'Fornecedores', COUNT(*) FROM fornecedor
                UNION ALL
                SELECT 'Vendas', COUNT(*) FROM venda
                UNION ALL
                SELECT 'Itens de Venda', COUNT(*) FROM item_venda
                UNION ALL
                SELECT 'Estoque', COUNT(*) FROM estoque
                UNION ALL
                SELECT 'Compras', COUNT(*) FROM compra
                UNION ALL
                SELECT 'Itens de Compra', COUNT(*) FROM item_compra
                UNION ALL
                SELECT 'Avaliações', COUNT(*) FROM avaliacao
                UNION ALL
                SELECT 'Promoções', COUNT(*) FROM promocao
                UNION ALL
                SELECT 'Produtos em Promoção', COUNT(*) FROM produto_promocao;
                """
                results = sql_handler.execute_query(query)
                if not results:
                    print("Nenhum dado encontrado.")
                    return
                print("\nTabela                 | Total de Registros")
                print("-----------------------|------------------")
                for row in results:
                    print(f"{row['Tabela']: <23}| {row['Total']}")

            def sales_by_store(sql_handler):
                query = """
                SELECT l.nome_loja, COUNT(v.id_venda) as total_vendas, SUM(v.valor_total) as valor_total
                FROM loja l
                LEFT JOIN venda v ON l.id_loja = v.id_loja
                GROUP BY l.id_loja, l.nome_loja
                ORDER BY valor_total DESC;
                """
                results = sql_handler.execute_query(query)
                if not results:
                    print("Nenhum dado encontrado.")
                    return
                print("\nLoja                     | Total de Vendas | Valor Total")
                print("-------------------------|-----------------|------------")
                for row in results:
                    print(f"{row['nome_loja']: <25}| {row['total_vendas']: <15}| R$ {row['valor_total']: <10.2f}")

            def top_selling_products(sql_handler):
                query = """
                SELECT p.nome_produto, SUM(iv.quantidade) as quantidade_vendida, SUM(iv.valor_total) as valor_total
                FROM produto p
                JOIN item_venda iv ON p.id_produto = iv.id_produto
                GROUP BY p.id_produto, p.nome_produto
                ORDER BY quantidade_vendida DESC
                LIMIT 10;
                """
                results = sql_handler.execute_query(query)
                if not results:
                    print("Nenhum dado encontrado.")
                    return
                print("\nProduto                    | Quantidade Vendida | Valor Total")
                print("---------------------------|--------------------|------------")
                for row in results:
                    print(f"{row['nome_produto']: <26}| {row['quantidade_vendida']: <19}| R$ {row['valor_total']: <10.2f}")

            def top_customers(sql_handler):
                query = """
                SELECT c.nome, COUNT(v.id_venda) as total_compras, SUM(v.valor_total) as valor_total
                FROM cliente c
                JOIN venda v ON c.id_cliente = v.id_cliente
                GROUP BY c.id_cliente, c.nome
                ORDER BY valor_total DESC
                LIMIT 10;
                """
                results = sql_handler.execute_query(query)
                if not results:
                    print("Nenhum dado encontrado.")
                    return
                print("\nCliente                   | Total de Compras | Valor Total")
                print("--------------------------|------------------|------------")
                for row in results:
                    print(f"{row['nome']: <26}| {row['total_compras']: <17}| R$ {row['valor_total']: <10.2f}")

            while True:
                print_reports_menu()
                report_choice = input("Escolha uma opção: ").strip()
                if report_choice == '1':
                    total_records(sql_handler)
                elif report_choice == '2':
                    sales_by_store(sql_handler)
                elif report_choice == '3':
                    top_selling_products(sql_handler)
                elif report_choice == '4':
                    top_customers(sql_handler)
                elif report_choice == '0':
                    break
                else:
                    print("Opção inválida.")
        elif choice == '0':
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida.")

    # Fechar conexões
    zodb_handler.close()
    mongo_handler.close()
    sql_handler.close()

if __name__ == "__main__":
    main()
