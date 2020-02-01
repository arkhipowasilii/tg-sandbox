import sqlite3 as sqlite
from datetime import datetime
from pathlib import Path
from threading import Lock


def connect_dec(func):
    def wrapper(self, *args, **kwargs):
        with self._lock:
            self._connect = sqlite.connect(str(self._path))
            result = func(self, *args, **kwargs)
            self._connect.close()
            return result
    return wrapper

class DatabaseHandler:
    def __init__(self, path: Path):
        self._path = path
        self._connect = None
        self._lock = Lock()

    @connect_dec
    def get_username(self, table,  id_: int):
        raw = self._connect.execute(f"SELECT username FROM '{table}' where id = {id_}").fetchone()
        return raw[0] if raw is not None else None

    @connect_dec
    def insert(self, table: str, id_, username):
        sql = f"INSERT INTO '{table}' VALUES ({id_}, '{username}')"
        self._connect.execute(sql)
        self._connect.commit()

    @connect_dec
    def add_table(self, table: str, values: str):
        sql = f"CREATE TABLE {table} ({values})"
        self._connect.execute(sql)
        self._connect.commit()
        return values

class HistoryDatabaseHandler:
    def __init__(self, path: Path):
        self._path = path
        self._connect = None
        self._lock = Lock()

    def insert(self, t_id: int, time: datetime, option: int):
        pass
