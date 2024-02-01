from . import db

name_table = "products"

class Product:
    @classmethod
    def create(cls, **datas):
        return cls(db.insert_into_table(name_table, **datas))
    
    def __init__(self, id: int):
        self.id = id
        self.datas = db.select_primary_key(name_table, id)
        
    def __repr__(self):
        return f"Product({self.id})"
    
    def __str__(self):
        return f"Product with {self.datas}"
        

class Products:
    @classmethod
    def search_by_title(cls, query: str) -> tuple:
        pass