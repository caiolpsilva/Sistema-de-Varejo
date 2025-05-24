# Sistema de Gerenciamento de Produtos - Manual de Funcionamento

## 1. Visão Geral do Projeto
Este sistema é uma aplicação de gerenciamento de produtos para varejo, com interface de linha de comando (CLI). Ele oferece funcionalidades para gestão de produtos, controle de estoque, histórico de preços, vendas, promoções, avaliações de clientes, relatórios e análise temporal de dados de vendas.

O sistema utiliza múltiplos bancos de dados para diferentes propósitos:
- MySQL para dados relacionais principais (produtos, estoque, vendas, clientes, etc.)
- MongoDB para armazenamento de comentários e imagens de produtos
- ZODB para armazenamento persistente de objetos de produto com características adicionais

## 2. Instalação e Configuração
### Requisitos
- Python 3.x
- MySQL Server com banco de dados configurado (ex: Varejobase)
- MongoDB Server rodando localmente
- Bibliotecas Python listadas em `requirements.txt`

### Passos para instalação
1. Clone o repositório do projeto.
2. Instale as dependências Python:
   ```
   pip install -r retail_data_analysis/requirements.txt
   ```
3. Configure o banco MySQL com as tabelas necessárias (produtos, estoque, vendas, etc.).
4. Certifique-se que o MongoDB está rodando localmente.
5. Execute o sistema via terminal:
   ```
   python retail_data_analysis/main_new.py
   ```

## 3. Arquitetura do Sistema e Módulos

### main_new.py
- Ponto de entrada do sistema.
- Interface CLI com menus para diferentes funcionalidades.
- Inicializa os handlers para MySQL, MongoDB e ZODB.
- Controla o fluxo principal e chamadas para funções específicas.

### sql_handler.py
- Classe `MySQLHandler` para conexão e execução de queries no banco MySQL.
- Métodos para executar consultas, inserções, atualizações e deleções.
- Gerencia conexão e tratamento de erros.

### mongodb_handler.py
- Classe `MongoDBHandler` para conexão com MongoDB.
- Métodos para inserir e recuperar comentários e imagens de produtos.
- Utiliza GridFS para armazenamento de imagens.

### zodb_model.py
- Define a classe `Product` como objeto persistente com atributos e métodos para manipulação.
- Classe `ZODBHandler` para gerenciar o banco ZODB, adicionando, recuperando e atualizando produtos.

### temporal_analysis.py
- Classe `TemporalAnalysis` para análise temporal de dados de vendas.
- Métodos para plotar tendências históricas de preço e estoque.
- Método para previsão de vendas futuras usando regressão linear.

## 4. Guia de Uso

### Executando o sistema
- Execute o script principal:
  ```
  python retail_data_analysis/main_new.py
  ```
- Navegue pelos menus utilizando os números das opções.

### Menus e funcionalidades principais
1. **Gestão de Produtos**: Listar, buscar, adicionar, atualizar e remover produtos.
2. **Controle de Estoque**: Listar estoque e atualizar quantidades.
3. **Histórico de Preços**: Visualizar tendências históricas e previsão de vendas.
4. **Vendas**: Listar vendas registradas.
5. **Promoções**: Listar promoções ativas.
6. **Avaliações de Clientes**: Listar avaliações de produtos feitas por clientes.
7. **Relatórios**: Gerar relatórios diversos como total de registros, vendas por loja, produtos mais vendidos e clientes com maior volume de compras.

## 5. Detalhes dos Bancos de Dados

### MySQL
- Tabelas principais utilizadas:
  - `produto`, `categoria`, `estoque`, `venda`, `item_venda`, `cliente`, `loja`, `funcionario`, `fornecedor`, `compra`, `item_compra`, `avaliacao`, `promocao`, `produto_promocao`
- Armazena dados relacionais essenciais para o sistema.

### MongoDB
- Coleções:
  - `comments`: Armazena comentários de clientes por produto.
  - `images`: Armazena referências a imagens de produtos usando GridFS.

### ZODB
- Armazena objetos `Product` persistentes com atributos customizados.
- Utilizado para manipulação avançada de produtos com características adicionais.

## 6. Funcionalidades de Análise Temporal
- Visualização gráfica da tendência histórica de preços e estoque para produtos específicos.
- Previsão de vendas futuras baseada em dados históricos usando regressão linear.
- Utiliza bibliotecas pandas, matplotlib e scikit-learn.

## 7. Considerações Finais e Solução de Problemas
- Certifique-se que os bancos de dados MySQL e MongoDB estejam rodando antes de iniciar o sistema.
- Verifique as credenciais de conexão no arquivo `sql_handler.py`.
- Para problemas com visualização gráfica, confirme que o ambiente suporta janelas de plotagem.
- Para dúvidas ou melhorias, consulte o código fonte e documentação dos módulos.

---

Este manual visa fornecer uma visão completa e detalhada do funcionamento do sistema para facilitar seu uso e manutenção.

## 8. Atendimento aos Requisitos de Modelagem de Dados

O projeto atende aos requisitos de modelagem de dados conforme descrito abaixo:

- Foi criado um modelo objeto-relacional utilizando o ZODB para gerenciar produtos e suas características de forma persistente e eficiente.
- O MongoDB foi utilizado para armazenar dados não estruturados, como comentários de clientes e imagens, aproveitando sua flexibilidade para esse tipo de dado.
- Aspectos temporais foram implementados para permitir a análise histórica de preços e estoque, bem como a previsão de vendas futuras, utilizando técnicas de análise de séries temporais e regressão linear.

Essas escolhas arquiteturais garantem uma gestão robusta e eficiente dos diferentes tipos de dados presentes no sistema, atendendo aos requisitos funcionais e não funcionais do projeto.
