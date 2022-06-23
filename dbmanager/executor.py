import sqlite3


def shape_to_string(shape):
    return ", ".join([f"{name} {data_type}" for name, data_type in shape])


class Executor:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor
        self.cache = {}

    def close(self):
        pass

    def create_table(self, table_name, shape: list):
        modified_shape = [(name, f"{data_type}  {' '.join(modifiers)}") for name, data_type, modifiers in shape]

        column_string = shape_to_string(modified_shape)

        self.cursor.execute(f"CREATE TABLE {table_name} ({column_string})")

    def delete_table(self, table_name):
        self.cursor.execute("DROP TABLE ?", (table_name,))

    def select(self, table_name, column, where):
        query = f"SELECT {column} FROM {table_name} WHERE {where}"
        self.cursor.execute(query)

        return self.cursor.fetchall()

    def table_exists(self, table_name):
        return len(self.select(f"sqlite_master", "name", f"type='table' AND name='{table_name}'")) > 0

    def get_columns(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name})")

        return [entry[1] for entry in self.cursor.fetchall()]

    def add_row(self, table_name, entries: dict):
        headers = entries.keys()
        values = [f"'{value}'" if type(value) == str else value for value in entries.values()]

        query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(values)})"

        self.cursor.execute(query)

    def modify_row(self, table_name, constraints: dict, entries: dict):
        headers = entries.keys()
        values = [f"'{value}'" if type(value) == str else value for value in entries.values()]
        zipped = [f"{header} = {value}" for header, value in zip(headers, values)]

        conditions = " AND ".format(
            [f"{condition} = '{value}'" if type(value) == str else value for condition, value in entries.items()])

        query = f"UPDATE {table_name} SET {', '.join(zipped)} WHERE {conditions}'"
        self.cursor.execute(query)
