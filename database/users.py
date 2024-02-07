from typing import Optional, Dict, Any, List
from .products import Product, Products
from . import (db,
               user, 
               basket)

class User:
    """
    Represents a user and provides methods for interacting with the database.
    """

    @classmethod
    def create(cls, **kwargs: Any) -> "User":
        """
        Create a new user and insert the data into the database.

        Args:
            **kwargs: Keyword arguments representing user data (e.g., pseudo, password, etc.).

        Returns:
            User: A new User object representing the created user.
        """
        return cls(db.insert_into_table(user, **kwargs))

    @classmethod
    def verify_password(cls, pseudo: str, password: str) -> Optional["User"]:
        """
        Verify the password for a user with the given pseudo.

        Args:
            pseudo (str): The pseudo (username) of the user.
            password (str): The password to verify.

        Returns:
            Optional[User]: User object if authentication is successful; otherwise, None.
        """
        try:
            _user = User(db.unique_to_id(user, "pseudo", pseudo))
            if _user.password == password:
                return _user
            return None
        except ValueError:
            return None

    def __init__(self, id: int) -> None:
        """
        Initialize a User object with data retrieved from the database.

        Args:
            id (int): The unique identifier of the user.

        Returns:
            None
        """
        self._datas = db.select_primary_key(user, id)
        self._id = self._datas.get("id", 0)
        self._pseudo = self._datas.get("pseudo", "")
        self._password = self._datas.get("password", "")
        self._description = self._datas.get("description", "")
        self._picture = self._datas.get("picture", b"")
        
    def get_basket(self):
        rows = db.get_rows(basket, "user_id", self.id)
        products = Products([row[1] for row in rows])
        quantities = [row[2] for row in rows]
        commands = [Command(product, quantity) for product, quantity in zip(products, quantities)]
        return Basket(self, commands)

    def __bool__(self) -> bool:
        """
        Check if the User object is considered truthy.

        Returns:
            bool: Always True.
        """
        return True

    @property
    def datas(self) -> Dict[str, Any]:
        """
        Returns the dictionary containing all the user data.

        Returns:
            Dict[str, Any]: The user data.
        """
        return self._datas

    @property
    def id(self) -> int:
        """
        Returns the unique identifier of the user.

        Returns:
            int: The user identifier.
        """
        return self._id

    @property
    def pseudo(self) -> str:
        """
        Returns the pseudo (username) of the user.

        Returns:
            str: The user pseudo.
        """
        return self._pseudo

    @pseudo.setter
    def pseudo(self, value: str) -> None:
        """
        Sets the pseudo (username) of the user and updates the database.

        Args:
            value (str): The new pseudo of the user.

        Raises:
            ValueError: If the provided pseudo already exists in the database.
        """
        if not db.exists(user, "pseudo", value):
            db.set(user, "pseudo", self.id, value)
            self._pseudo = value
            return None
        raise ValueError("Existing username...")

    @property
    def password(self) -> str:
        """
        Returns the password of the user.

        Returns:
            str: The user password.
        """
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """
        Sets the password of the user and updates the database.

        Args:
            value (str): The new password of the user.
        """
        db.set(user, "password", self.id, value)
        self._password = value

    @property
    def description(self) -> str:
        """
        Returns the description of the user.

        Returns:
            str: The user description.
        """
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """
        Sets the description of the user and updates the database.

        Args:
            value (str): The new description of the user.
        """
        db.set(user, "description", self.id, value)
        self._description = value

    @property
    def picture(self) -> bytes:
        """
        Returns the binary data representing the picture of the user.

        Returns:
            bytes: The user picture data.
        """
        return self._picture

    @picture.setter
    def picture(self, value: bytes) -> None:
        """
        Sets the picture of the user and updates the database.

        Args:
            value (bytes): The new picture data of the user.
        """
        db.set(user, "picture", self.id, value)
        self._picture = value

    def delete(self) -> None:
        """
        Delete the user record from the database.
        """
        db.delete(user, self.id)

    def __repr__(self) -> str:
        """
        Return a string representation of the User object.

        Returns:
            str: A string representation.
        """
        return f"User({self.id})"

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the User object.

        Returns:
            str: A human-readable string representation.
        """
        return f"User with {self.datas}"


class Command:
    def __init__(self, user: User, product: Product, quantity: int):
        """
        Represents a user command to modify the quantity of a product in their basket.

        Args:
            user (User): The user associated with the command.
            product (Product): The product associated with the command.
            quantity (int): The quantity of the product in the command.

        Attributes:
            user (User): The user associated with the command.
            product (Product): The product associated with the command.
            quantity (int): The quantity of the product in the command.
        """
        self._user = user
        self._product = product
        self._quantity = quantity

    @property
    def user(self) -> User:
        """
        Get the user associated with the command.

        Returns:
            User: The user associated with the command.
        """
        return self._user

    @property
    def product(self) -> Product:
        """
        Get the product associated with the command.

        Returns:
            Product: The product associated with the command.
        """
        return self._product

    @property
    def quantity(self) -> int:
        """
        Get the quantity of the product in the command.

        Returns:
            int: The quantity of the product in the command.
        """
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """
        Set the quantity of the product in the command and update the database.

        Args:
            value (int): The new quantity of the product in the command.
        """
        db.delete_by_conditions(basket, ("user_id", "product_id"), (self.user.id, self.product.id))
        db.insert_into_table(basket, user_id=self.user.id, product_id=self.product.id, quantity=value)
        self._quantity = value


class Basket:
    def __init__(self, user: User, commands: List[Command]):
        """
        Represents a collection of user commands to modify product quantities in a basket.

        Args:
            commands (List[Command]): A list of Command objects.

        Attributes:
            commands (List[Command]): A list of Command objects.
        """
        self._commands = commands
        self._user = user

    @property
    def commands(self) -> List[Command]:
        """
        Get the list of commands in the basket.

        Returns:
            List[Command]: A list of Command objects in the basket.
        """
        return self._commands
    
    @property
    def user(self):
        return self._user

    def __getitem__(self, index: int) -> Command:
        """
        Get a specific command from the basket using the index.

        Args:
            index (int): The index of the command to retrieve.

        Returns:
            Command: The Command object at the specified index.
        """
        return self.commands[index]

    def __iter__(self) -> List[Command]:
        """
        Enable iteration over the commands in the basket.

        Returns:
            Iterator: An iterator over the commands in the basket.
        """
        return iter(self.commands)

    def __bool__(self) -> bool:
        """
        Check if the basket has any commands.

        Returns:
            bool: True if the basket has commands, False otherwise.
        """
        return bool(self.commands)
    
    def delete(self, product:Product|None=None, index:int|None=None, command:Command|None=None) -> None:
        if product is not None:
            db.delete_by_conditions(basket, ("user_id", "product_id"), (self.user.id, product.id))
            self = self.user.get_basket()
        elif index is not None:
            db.delete_by_conditions(basket, ("user_id", "product_id"), (self.user.id, self[index].product.id))
        elif command is not None:
            db.delete_by_conditions(basket, ("user_id", "product_id"), (self.user.id, command.product.id)) 
        else:
            raise ValueError("No valid argument given.")
        
    def add(self, product:Product, quantity:int=1):
        try:
            index = [command.product for command in self.commands].index(product)
            self.commands[index].quantity += quantity
        except:
            db.insert_into_table(basket, user_id=self.user.id, product_id=product.id, quantity=quantity)
        
       

