import sqlite3 as sqlite
from pathlib import Path


class DatabaseHandler:
    def __init__(self, path: Path):
        self._connect = sqlite.connect(str(path))

    def __del__(self):
        self._connect.close()

    def get_username(self, table,  id_: int):
        raw = self._connect.execute(f"SELECT username FROM '{table}' where id = {id_}").fetchone()
        return raw[0] if raw is not None else None

    def insert(self, table: str, id_, username):
        sql = f"INSERT INTO '{table}' VALUES ({id_}, '{username}')"
        self._connect.execute(sql)
        self._connect.commit()

    def add_table(self, table: str, values: str):
        sql = f"CREATE TABLE {table} ({values})"
        self._connect.execute(sql)
        self._connect.commit()
        return values


if __name__ == '__main__':
    db = Path("C:\\") / "Users" / "Intel Core i7" / "PycharmProjects" / "tg-sandbox" / "telegram.db"
    assert db.exists()
    hndl = DatabaseHandler(db)
    table_name = "users"

    print(hndl.get_username(table_name, 3))

