import sqlite3 as sqlite
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import List, Tuple, Iterable


def connect_dec(func):
    def wrapper(self, *args, **kwargs):
        with self._lock:
            self._connect = sqlite.connect(str(self._path))
            result = func(self, *args, **kwargs)
            self._connect.commit()
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

    @connect_dec
    def add_table(self, table: str, values: str):
        sql = f"CREATE TABLE {table} ({values})"
        self._connect.execute(sql)
        return values


class HistoryDatabaseHandler:
    def __init__(self, path: Path):
        self._path = path
        self._connect = None
        self._lock = Lock()
        self.table = 'history'

    @connect_dec
    def insert(self, t_id: int, time: datetime, options: List[int]):
        options = ','.join(f"({t_id}, '{time}', {num})" for num in options)
        sql = f"INSERT INTO '{self.table}' VALUES {options}"
        print(sql)
        self._connect.execute(sql)

    @connect_dec
    def add_table(self, table: str, values: str):
        sql = f"CREATE TABLE {table} ({values})"
        self._connect.execute(sql)
        return values

    @connect_dec
    def get_history(self, t_id: int) -> Iterable[Tuple[datetime, str]]:
        raw = self._connect.execute(f"SELECT datatime, button FROM '{self.table}' where t_id = {t_id}").fetchall()
        return ((datetime.fromisoformat(dt), bt) for dt, bt in raw)

    @connect_dec
    def delete_history(self, t_id: int):
        sql = f"DELETE from '{self.table}' where t_id = {t_id}"
        self._connect.execute(sql)
