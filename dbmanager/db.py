import sqlite3

from os.path import join

from .executor import Executor
from .table import Table


class DB:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.file_path = join(path, name)

        self.conn = sqlite3.connect(self.file_path)
        self.cursor = self.conn.cursor()
        self.executor = Executor(self.cursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.close()

    def get_table(self, table_name):
        return Table(self.executor, table_name) if self.executor.table_exists(table_name) else None

    def create_table(self, table_name, shape):
        self.executor.create_table(table_name, shape)

        return Table(self.executor, table_name)

    def has_table(self, table_name):
        return self.executor.table_exists(table_name)

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()
