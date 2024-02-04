from . import db
from typing import List, Tuple, Any, Dict

name_table = "products"

class Product:
    """
    Represents a product with information stored in a database.

    Attributes:
        _id (int): The unique identifier of the product.
        _datas (Dict[str, Any]): A dictionary containing all the product data retrieved from the database.
        _name (str): The name of the product.
        _description (str): The description of the product.
        _price (float): The price of the product.
        _quantity (float): The quantity of the product.
        _illustration (bin): The binary data representing the illustration of the product.
    """

    @classmethod
    def create(cls, **datas: Any) -> 'Product':
        """
        Creates a new instance of the Product class and inserts data into the database.

        Args:
            **datas: Keyword arguments representing the product data.

        Returns:
            Product: The newly created Product instance.
        """
        return cls(db.insert_into_table(name_table, **datas))

    def __init__(self, id: int) -> None:
        """
        Initializes a Product instance by retrieving data from the database.

        Args:
            id (int): The unique identifier of the product.
        """
        self._datas = db.select_primary_key(name_table, id)
        self._id = self._datas["id"]
        self._name = self._datas["name"]
        self._description = self._datas["description"]
        self._price = self._datas["price"]
        self._quantity = self._datas["quantity"]
        self._illustration = self._datas["illustration"]

    @property
    def datas(self) -> Dict[str, Any]:
        """
        Returns the dictionary containing all the product data.

        Returns:
            Dict[str, Any]: The product data.
        """
        return self._datas

    @property
    def id(self) -> int:
        """
        Returns the unique identifier of the product.

        Returns:
            int: The product identifier.
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Returns the name of the product.

        Returns:
            str: The product name.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Sets the name of the product and updates the database.

        Args:
            value (str): The new name of the product.

        Raises:
            ValueError: If the provided name already exists in the database.
        """
        if not db.exists(name_table, "name", value):
            db.set(name_table, "name", self.id, value)
            self._name = value
            return None
        raise ValueError("Existing product name...")


    @property
    def description(self) -> str:
        """
        Returns the description of the product.

        Returns:
            str: The product description.
        """
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """
        Sets the description of the product and updates the database.

        Args:
            value (str): The new description of the product.
        """
        db.set(name_table, "description", self.id, value)
        self._description = value

    @property
    def price(self) -> float:
        """
        Returns the price of the product.

        Returns:
            float: The product price.
        """
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """
        Sets the price of the product and updates the database.

        Args:
            value (float): The new price of the product.
        """
        db.set(name_table, "price", self.id, value)
        self._price = value

    @property
    def quantity(self) -> float:
        """
        Returns the quantity of the product.

        Returns:
            float: The product quantity.
        """
        return self._quantity

    @quantity.setter
    def quantity(self, value: float) -> None:
        """
        Sets the quantity of the product and updates the database.

        Args:
            value (float): The new quantity of the product.
        """
        db.set(name_table, "quantity", self.id, value)
        self._quantity = value

    @property
    def illustration(self) -> bin:
        """
        Returns the binary data representing the illustration of the product.

        Returns:
            bin: The product illustration data.
        """
        return self._illustration

    @illustration.setter
    def illustration(self, value: bin) -> None:
        """
        Sets the illustration of the product and updates the database.

        Args:
            value (bin): The new illustration data of the product.
        """
        db.set(name_table, "illustration", self.id, value)
        self._illustration = value

    def __repr__(self) -> str:
        """
        Returns a string representation of the Product instance.

        Returns:
            str: A string representation of the product.
        """
        return f"Product({self.id})"

    def __str__(self) -> str:
        """
        Returns a string representation of the Product instance with all its data.

        Returns:
            str: A string representation of the product with all its data.
        """
        return f"Product with {self.datas}"
    
    def __bool__(self) -> bool:
        return True
    
    def delete(self) -> None:
        """
        Delete the product record from the database.
        """
        return db.delete(name_table, self.id)



class Products:
    """
    Represents a collection of products.

    Attributes:
        _products (List[Product]): List of Product instances in the collection.
    """

    def __init__(self, products: List[Product]) -> None:
        """
        Initializes a Products instance with a list of Product instances.

        Args:
            products (List[Product]): List of Product instances.
        """
        self._products = products

    def __getitem__(self, index: int) -> Product:
        """
        Retrieves a Product instance at the specified index.

        Args:
            index (int): Index of the Product instance.

        Returns:
            Product: The Product instance at the specified index.
        """
        return self._products[index]

    def __repr__(self) -> str:
        """
        Returns a string representation of the Products instance.

        Returns:
            str: A string representation of the Products instance.
        """
        return f"Products({str(self._products)})"

    def __str__(self) -> str:
        """
        Returns a string representation of the Products instance.

        Returns:
            str: A string representation of the Products instance.
        """
        return str(self._products)

    def __iter__(self) -> iter:
        """
        Returns an iterator for the Products instance.

        Returns:
            iter: An iterator for the Products instance.
        """
        return iter(self._products)

    def filter_by_price(self, min_price: float | None = None, max_price: float | None = None) -> "Products":
        """
        Filters products based on the specified price range.

        Args:
            min_price (float | None): Minimum price for filtering.
            max_price (float | None): Maximum price for filtering.

        Returns:
            Products: A new Products instance containing the filtered products.
        """
        match (min_price, max_price):
            case (None, None):
                return self
            case (_, None):
                return Products([product for product in self if min_price <= product.price])
            case (None, _):
                return Products([product for product in self if product.price <= max_price])
            case (_, _):
                return Products([product for product in self if min_price <= product.price <= max_price])

    @classmethod
    def get(cls, products: List[Tuple[int]]) -> "Products":
        """
        Creates a Products instance from a list of product IDs.

        Args:
            products (List[Tuple[int]]): List of tuples containing product IDs.

        Returns:
            Products: A new Products instance.
        """
        return Products([Product(product_id) for product_id, *_ in products])

    @classmethod
    def search_by_name(cls, query: str, sort_by: str | None = None, desc: bool = False) -> "Products":
        """
        Searches products by name and returns a Products instance.

        Args:
            query (str): Search query for product names.
            sort_by (str | None): Attribute to sort the results by.
            desc (bool): Flag indicating whether to sort in descending order.

        Returns:
            Products: A new Products instance containing the search results.
        """
        result = db.search_into(name_table, ("name", ), query, sort_by, desc)
        return cls.get(result)

    @classmethod
    def search_by_description(cls, query: str, sort_by: str | None = None, desc: bool = False) -> "Products":
        """
        Searches products by description and returns a Products instance.

        Args:
            query (str): Search query for product descriptions.
            sort_by (str | None): Attribute to sort the results by.
            desc (bool): Flag indicating whether to sort in descending order.

        Returns:
            Products: A new Products instance containing the search results.
        """
        result = db.search_into(name_table, ("description", ), query, sort_by, desc)
        return cls.get(result)

    @classmethod
    def search(cls, query: str, sort_by: str | None = None, desc: bool = False, min_price: float | None = None,
               max_price: float | None = None) -> "Products":
        """
        Searches products by name and description, and filters the results based on price range.

        Args:
            query (str): Search query for product names and descriptions.
            sort_by (str | None): Attribute to sort the results by.
            desc (bool): Flag indicating whether to sort in descending order.
            min_price (float | None): Minimum price for filtering.
            max_price (float | None): Maximum price for filtering.

        Returns:
            Products: A new Products instance containing the search and filtered results.
        """
        result = db.search_into(name_table, ("name", "description"), query, sort_by, desc)
        return cls.get(result).filter_by_price(min_price, max_price)
