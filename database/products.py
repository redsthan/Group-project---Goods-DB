from . import db
from typing import List

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
    def search_by_name(cls, query: str, sort_by: str|None = None) -> List[Product]:
        result = db.search_into(name_table, ("name", ), query, sort_by)
        print(result)
        return [Product(id) for id, *_ in result]