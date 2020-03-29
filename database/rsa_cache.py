from database.db import DBConn


class RSACache(DBConn):
    _create_sql = "CREATE TABLE IF NOT EXISTS rsa_cache"
    _create_sql += " (id INTEGER PRIMARY KEY AUTOINCREMENT, private TEXT, public TEXT, is_reserved INTEGER)"

    _create_index = "CREATE INDEX IF NOT EXISTS key_index ON rsa_cache (id)"
    _get_all_ids = "SELECT id FROM rsa_cache WHERE id > ?"
    _get_by_id_sql = "SELECT private, public FROM rsa_cache WHERE id = ?"
    _get_is_reserved = "SELECT is_reserved FROM rsa_cache WHERE id = ?"
    _get_unreserved_keypairs = "SELECT id FROM rsa_cache WHERE is_reserved = 0"
    _insert_sql = "INSERT INTO rsa_cache (private, public, is_reserved) VALUES (?, ?, 0)"
    _reserve_keypair_sql = "UPDATE rsa_cache SET is_reserved = 1 WHERE id = ?"

    _del_all_sql = "DELETE FROM rsa_cache"

    def __init__(self):
        super().__init__(db_path="./database/db.sqlite")
        self.init_table(self._create_sql, self._create_index)

        self.test_connection('rsa_cache')

    def get_all_keypair_ids(self, after_id: int = 0):
        rows = self.execute_query(self._get_all_ids, after_id)
        return [row["id"] for row in rows]

    def get_unreserved_keypair_ids(self):
        rows = self.execute_query(self._get_unreserved_keypairs)
        return [row["id"] for row in rows]

    def get_key_pair(self, keypair_id: str):
        row = self.execute_query(self._get_by_id_sql, keypair_id)[0]
        return row["private"], row["public"]

    def is_reserved(self, key_pair_id: str):
        result = self.execute_query(self._get_is_reserved, key_pair_id)["is_reserved"]
        return bool(int(result))

    def insert_key_pair(self, private_key: str, public_key: str):
        return self.execute_and_return_id(self._insert_sql, private_key, public_key)

    def reserve_key_pair(self, key_pair_id: str):
        if not self.is_reserved(key_pair_id):
            self.execute_query(self._reserve_keypair_sql, key_pair_id)

    def delete_all(self):
        self.execute_query(self._del_all_sql)