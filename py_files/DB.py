import psycopg2
import os


class DB:
    """
    A simple DB Class used to interact with Postgres database.
    DB = Data Access Object
    """
    def __init__(self) -> None:
        """
        Starts a connection with DB, some env vars need to be set before call it.
        self.host = os.environ['POSTGRES_HOST']
        self.port = os.environ['POSTGRES_PORT']
        self._user = os.environ['POSTGRES_USER']
        self._password = os.environ['POSTGRES_PASSWORD']
        self.database = os.environ['POSTGRES_DB']
        :return None
        """
        self.host = os.environ['POSTGRES_HOST']
        self.port = os.environ['POSTGRES_PORT']
        self.user = os.environ['POSTGRES_USER']
        self.password = os.environ['POSTGRES_PASSWORD']
        self.database = os.environ['POSTGRES_DB']
        self.db_conn = None
        self.db_cursor = None

    def init_connection(self) -> None:
        """
        Uses self attributes to start a connection with DB.
        :return: None, but it can raise an exception in case connection fails.
        """
        try:
            self.db_conn = psycopg2.connect(dbname=self.database,
                                            user=self.user,
                                            password=self.password,
                                            host=self.host,
                                            port=self.port)
            self.db_cursor = self.db_conn.cursor()
        except Exception as e:
            raise ConnectionError(f'Unable to connect on {self.host}:{self.port}.\n'
                                  f'Error: \n{e.args}') from e

    def stop_connection(self) -> None:
        """
        Just closes self DB connection
        :return: None
        """
        self.db_cursor.close()
        self.db_conn.close()
        self.db_conn = None
        self.db_cursor = None

    def check_connection(self) -> None:
        """
        Renew the connection if it is not ok
        :return: None
        """
        if self.db_conn is None:
            self.init_connection()

    def execute_query(self, query: str, commit=False, fetch=False) -> list:
        """
        Execute an SQL query on DB
        :param query: SQL query to be executed.
        :param commit: True if you want tp commit, False if you don't want to.
        :param fetch: Enable to return the query output.
        :return: List in case of fetch is True, None if it is not.
        """
        self.check_connection()
        try:
            self.db_cursor.execute(query)
        except Exception as exc:
            print(query)
            raise exc
        if commit:
            self.commit()
        if fetch:
            return self.db_cursor.fetchall()

    def commit(self) -> None:
        """
        Just commit querys already executed.
        :return: None
        """
        self.db_conn.commit()

    @staticmethod
    def db_setup(path) -> None:
        """
        Static method to setup the database
        :param path: sql file to setup the database.
        """
        db = DB()
        with open(path) as file:
            sql_schema = file.read()
            db.execute_query(sql_schema, commit=True)
