import sqlite3

from database.db import DBConn
from models.user import DBUserSession


class UserCache(DBConn):
    _create_sql = "CREATE TABLE IF NOT EXISTS user_cache"
    _create_sql += " (user_id TEXT PRIMARY KEY, session_token TEXT, km_token TEXT, parent_id TEXT)"

    _create_index = "CREATE INDEX IF NOT EXISTS key_index ON user_cache (user_id)"
    _get_all_sql = "SELECT * FROM user_cache"
    _get_user_sql = "SELECT * FROM user_cache WHERE user_id = ?"
    _get_users_sql = "SELECT * FROM user_cache WHERE parent_id = ?"
    _del_all_sql = "DELETE FROM user_cache"
    _insert_sql = "INSERT INTO user_cache (user_id, session_token, km_token, rsa_id, parent_id) VALUES (?, ?, ?, ?, ?)"
    _update_sql = "REPLACE INTO user_cache (user_id, session_token, km_token, rsa_id, parent_id) VALUES (?, ?, ?, ?, ?)"

    def __init__(self):
        super().__init__(db_path="./database/db.sqlite")
        self.init_table(self._create_sql, self._create_index)

        self.test_connection('user_cache')

    def get_user_session(self, sym_user_id: str):
        row = self.execute_query(self._get_user_sql, sym_user_id)[0]
        return DBUserSession(row)

    def get_parent_users(self):
        return self.get_users_by_parent()

    def get_users_by_parent(self, parent_id: str = None):
        rows = self.execute_query(self._get_users_sql, parent_id)
        return [DBUserSession(row) for row in rows]

    def insert_user_session(self, sym_id, session_token, km_token, rsa_id, parent_id=None):
        self.execute_query(self._insert_sql, sym_id, session_token, km_token, rsa_id, parent_id)

    def update_user_session(self, sym_user_id, session_token, km_token, rsa_id, parent_id):
        self.execute_query(self._update_sql, sym_user_id, session_token, km_token, rsa_id, parent_id)

    def upsert_user_session(self, sym_user_id, session_token, km_token, rsa_id, parent_id):
        try:
            self.insert_user_session(sym_user_id, session_token, km_token, rsa_id, parent_id)
        except sqlite3.IntegrityError:
            self.update_user_session(sym_user_id, session_token, km_token, rsa_id, parent_id)

    def clear_all(self):
        self.execute_query(self._del_all_sql)
