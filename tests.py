from database import products

r = products.Product.create(name="truc")
y = products.Product(2)
print(r, y)