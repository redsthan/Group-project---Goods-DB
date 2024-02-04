from typing import Optional, Dict, Any
from . import db

name_table = "users"

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
        return cls(db.insert_into_table(name_table, **kwargs))

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
            user = User(db.unique_to_id(name_table, "pseudo", pseudo))
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
        self._datas = db.select_primary_key(name_table, id)
        self._id = self._datas.get("id", 0)
        self._pseudo = self._datas.get("pseudo", "")
        self._password = self._datas.get("password", "")
        self._description = self._datas.get("description", "")
        self._picture = self._datas.get("picture", b"")

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
        """
        db.set(name_table, self.id, "pseudo", value)
        self._pseudo = value

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
        db.set(name_table, self.id, "password", value)
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
        db.set(name_table, self.id, "description", value)
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
        db.set(name_table, self.id, "picture", value)
        self._picture = value

    def delete(self) -> None:
        """
        Delete the user record from the database.
        """
        db.delete(name_table, self.id)

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
