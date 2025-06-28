import sqlite3


class SQLite:

    def __init__(
        self,
        db_name="",
    ) -> None:
        """
        """
        self.connection: sqlite3.Connection = sqlite3.connect(database=db_name)
        self.cursor: sqlite3.Cursor = self.connection.cursor()
