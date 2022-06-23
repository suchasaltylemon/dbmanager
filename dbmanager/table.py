class Table:
    def __init__(self, executor, table_name):
        self.executor = executor
        self.table_name = table_name

    def _tuple_to_dict(self, data):
        dictionary = {}
        columns = self.executor.get_columns(self.table_name)

        for column, value in zip(columns, data):
            dictionary[column] = value

        return dictionary

    def get_row(self, constraints: dict):
        constraint_string = ", ".join(
            [f"{column} = " + (f"'{value}'" if type(value) == str else f"{value}") for column, value in
             constraints.items()])

        raw = self.executor.select(self.table_name, "*", constraint_string)

        return self._tuple_to_dict(raw[0] if len(raw) > 0 else {})

    def add_row(self, data):
        self.executor.add_row(self.table_name, data)

    def update_row(self, constraints, data):
        self.executor.modify_row(self.table_name, constraints, data)

    def has_row(self, constraints: dict):
        return len(self.get_row(constraints)) > 0
