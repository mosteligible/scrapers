from venv import create
import mysql.connector as ctx
from log import create_logger


class DatabaseCtx:
    def __init__(self, username: str, password: str, host: str, database: str):
        self._username = username
        self._password = password
        self._host = host
        self._connection = None
        self.reconnect(database=database)
        self.logger = create_logger(logger_name="DOWNLOADS", file_name="downloads_log")

    def add_entry(self, advertisement: dict, table_name: str) -> None:
        insert_query = f"INSERT INTO {table_name}"
        column_names = ", ".join([
            f"`{col_name}`" 
            for col_name in advertisement.keys()
            ])
        values_for_column = ", ".join([
            "'{}'".format(val.replace('\'', '\'\''))
            if type(val) == str else f"'{val}'"
            for val in advertisement.values()
            ])
        query = f"{insert_query} ({column_names}) VALUES ({values_for_column})"
        self.logger.info(f"{table_name} - query - {query}")
        self._cursor.execute(query)
        self._connection.commit()

    def reconnect(self, database: str):
        if self._connection:
            self._cursor.close()
            self._connection.close()
        self._connection = ctx.connect(
            user=self._username,
            password=self._password,
            host=self._host,
            database=database
        )
        self._cursor = self._connection.cursor(named_tuple=True)

    def is_connected(self):
        return self._connection.is_connected()
