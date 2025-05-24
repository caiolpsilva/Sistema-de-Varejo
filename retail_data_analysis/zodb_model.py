from persistent import Persistent
from ZODB import FileStorage, DB
import transaction

class Product(Persistent):
    def __init__(self, product_id, name, category, price, stock):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.characteristics = {}

    def add_characteristic(self, key, value):
        self.characteristics[key] = value

    def update_price(self, new_price):
        self.price = new_price

    def update_stock(self, new_stock):
        self.stock = new_stock

class ZODBHandler:
    def __init__(self, db_path='retail_data.fs'):
        self.storage = FileStorage.FileStorage(db_path)
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()

        if 'products' not in self.root:
            self.root['products'] = {}

    def add_product(self, product):
        self.root['products'][product.product_id] = product
        transaction.commit()

    def get_product(self, product_id):
        return self.root['products'].get(product_id)

    def update_product(self, product_id, **kwargs):
        product = self.get_product(product_id)
        if not product:
            return False
        for key, value in kwargs.items():
            setattr(product, key, value)
        transaction.commit()
        return True

    def close(self):
        self.connection.close()
        self.db.close()
        self.storage.close()
