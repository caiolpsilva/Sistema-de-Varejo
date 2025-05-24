import mysql.connector
from mysql.connector import Error

class MySQLHandler:
    def __init__(self, host='localhost', user='root', password='30376619Caio', database='Varejobase'):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                print("Conectado ao banco MySQL VarejoBase")
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            self.connection = None

    def execute_query(self, query, params=None):
        if not self.connection:
            print("Sem conexão com MySQL")
            return None
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
                return result
            else:
                self.connection.commit()
                return cursor.rowcount
        except Error as e:
            print(f"Erro ao executar query: {e}")
            return None
        finally:
            cursor.close()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexão MySQL encerrada")

    def get_product_by_id(self, product_id):
        query = "SELECT * FROM produto WHERE id_produto = %s"
        result = self.execute_query(query, (product_id,))
        if result and len(result) > 0:
            return result[0]
        return None
