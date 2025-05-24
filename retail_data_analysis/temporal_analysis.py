import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class TemporalAnalysis:
    def __init__(self, sales_data):
        """
        sales_data: pandas DataFrame with columns ['date', 'product_id', 'price', 'stock', 'sales']
        """
        self.sales_data = sales_data
        self.sales_data['date'] = pd.to_datetime(self.sales_data['date'])

    def historical_price_trend(self, product_id):
        df = self.sales_data[self.sales_data['product_id'] == product_id]
        df = df.sort_values('date')
        plt.figure(figsize=(10,5))
        plt.plot(df['date'], df['price'], marker='o')
        plt.title(f'Tendência Histórica de Preço do Produto {product_id}')
        plt.xlabel('Data')
        plt.ylabel('Preço')
        plt.grid(True)
        plt.show()
        input("Pressione Enter para continuar...")

    def historical_stock_trend(self, product_id):
        df = self.sales_data[self.sales_data['product_id'] == product_id]
        df = df.sort_values('date')
        plt.figure(figsize=(10,5))
        plt.plot(df['date'], df['stock'], marker='o', color='orange')
        plt.title(f'Tendência Histórica de Estoque do Produto {product_id}')
        plt.xlabel('Data')
        plt.ylabel('Estoque')
        plt.grid(True)
        plt.show()
        input("Pressione Enter para continuar...")

    def forecast_sales(self, product_id, days=30):
        df = self.sales_data[self.sales_data['product_id'] == product_id]
        df = df.sort_values('date')
        df = df[df['sales'] > 0]  # Garante que só usa vendas > 0

        if len(df) < 2:
            print("Não há dados suficientes para previsão de vendas.")
            return

        # Converte datas para ordinal para regressão
        X = df['date'].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
        y = df['sales'].values

        if len(X) == 0 or len(y) == 0:
            print("Não há dados suficientes para previsão de vendas.")
            return

        model = LinearRegression()
        model.fit(X, y)

        future_dates = pd.date_range(df['date'].max(), periods=days+1)[1:]
        future_ordinals = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
        forecast = model.predict(future_ordinals)

        plt.figure(figsize=(10,5))
        plt.plot(df['date'], y, label='Vendas Históricas')
        plt.plot(future_dates, forecast, label='Previsão de Vendas', linestyle='--')
        plt.title(f'Previsão de Vendas para o Produto {product_id}')
        plt.xlabel('Data')
        plt.ylabel('Vendas')
        plt.legend()
        plt.grid(True)
        plt.show()
        input("Pressione Enter para continuar...")
        return future_dates, forecast
