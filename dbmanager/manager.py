from .db import DB


class Manager:
    def __init__(self, path):
        self.path = path

        self.databases = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.close()

    def refresh(self):
        pass

    def get_database(self, name) -> DB:
        if name not in self.databases:
            self.databases[name] = DB(self.path, f"{name}.db")

        return self.databases[name]

    def create_database(self, name):
        pass

    def commit(self):
        for db in self.databases.values():
            db.commit()

    def close(self):
        for db in self.databases.values():
            db.close()
