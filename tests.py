#Pour la gestion de produits
from database.products import Products, Product 
#Pour la gestion d'utilisateurs
from database.users import User

#product = Product.create(name="Figurine Mario")
print(Products.search("Mario")[0])