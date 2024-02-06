from typing import Optional, Dict, Any
from . import (db, 
               Product,
               Products, 
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
            user = User(db.unique_to_id(user, "pseudo", pseudo))
            if user.password == password:
                return user
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
        
    def get_basket(self) -> Products:
        """
        Retrieve the products in the user's basket from the database.

        Returns:
            Products: A Products object representing the items in the user's basket.
            
        Note:
            The Products collection may be empty if the user's basket is currently empty.
        """
        products = Products([row[1] for row in db.get_rows(basket, "user_id", self.id)])
        return products
    
    def add_to_basket(self, product: Product, quantity:int=1) -> None:
        """
        Add a product to the user's basket in the database.

        Args:
            product (Product): The product to add to the basket.
            quantity (int, optional): The quantity of the product to add (default is 1).

        Raises:
            ValueError: If the quantity is not a positive integer.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        db.insert_into_table(basket, user_id=self.id, product_id=product.id, quantity=quantity)
    
    def remove_from_basket(self, product: Product) -> None:
        """
        Remove a product from the user's basket in the database.

        Args:
            product (Product): The product to remove from the basket.

        Note:
            If the specified product is not found in the user's basket, no action is taken.
        """
        db.delete_by_conditions(basket, ("user_id", "product_id"), (self.id, product.id))

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
