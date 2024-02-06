from .request.request import DataBase
from pathlib import Path

user = "user"
basket = "basket"
product = "product"

script_directory = Path(__file__).parent

map_path = script_directory / "requests" / "creation.sql"
db_path = script_directory / "database.db"

db = DataBase(db_path)
db.executefile(map_path)