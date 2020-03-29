import sqlite3

from pathlib import Path

# I don't think SQLite supports conneciton pooling, so I'm just going to
# share the conneciton between the classes at the module level to avoid
# opening and closing them
database_connection = None


class DBConn:
    def __init__(self, db_path: str = None):
        self.database_path = Path(db_path)
        self.conn = self.open_connection()

    def open_connection(self):
        global database_connection

        if not database_connection:
            database_connection = sqlite3.Connection(self.database_path, timeout=60)
            database_connection.row_factory = sqlite3.Row

        return database_connection

    def init_table(self, create_sql: str, create_index_sql: str):
        with self.conn as cn:
            cn.execute(create_sql)
            cn.execute(create_index_sql)

    def execute_query(self, query: str, *values):
        with self.conn as cn:
            return cn.execute(query, tuple(values))

    def execute_and_return_id(self, query: str, *values):
        with self.conn as cn:
            cur = cn.cursor()
            cur.execute(query, tuple(values))

            return cur.lastrowid

    def test_connection(self, table_name: str):
        try:
            self.execute_query(f"SELECT 1 FROM {table_name} LIMIT 1")

            return True
        except sqlite3.ProgrammingError as sqlite_ex:
            print(sqlite_ex)

        return False
