from . import db
from typing import Dict, Any


name_table = "users"

class User:
    @classmethod
    def create(cls, **kwargs: Any) -> "User":
        return cls(db.insert_into_table(name_table, **kwargs))
    
    @classmethod
    def verify_password(cls, pseudo:str, password:str) -> bool|"User":
        
    
    def __init__(self, id: int) -> None:
        self._datas = db.select_primary_key(name_table, id)
        self._id = self._datas["id"]
        self._pseudo = self._datas["pseudo"]
        self._password = self._datas["password"]
        self._description = self._datas["description"]
        self._picture = self._datas["picture"]

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
    def picture(self) -> bin:
        """
        Returns the binary data representing the picture of the user.

        Returns:
            bin: The user picture data.
        """
        return self._picture

    @picture.setter
    def picture(self, value: bin) -> None:
        """
        Sets the picture of the user and updates the database.

        Args:
            value (bin): The new picture data of the user.
        """
        db.set(name_table, self.id, "picture", value)
        self._picture = value
