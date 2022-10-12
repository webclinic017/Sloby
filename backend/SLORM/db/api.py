# standard library imports
import logging
# third party imports
from psycopg import Connection, connect, errors
from typing import List

# this project

from .db_config.config import config

logger = logging.getLogger("sloby.db")


class SlobyDB:
    def __init__(self, conf=None, tables: list[dict[str, str]] = None, show_tables: bool = False):
        """Initialize database from config
        Args:
            tables list[dict[str, str]] = None: A list with dictionaries, that contain the name of the table and the data of the table.
            show_tables: bool = False: if the show_tables is true then you going to get a message in the terminal about the tables(all)
        """

        if conf is None:
            self.conf = config()
        else:
            self.conf = conf

        if tables is None:
            self.tables = []
            logger.info("Empty table fields!!!")
        else:
            self.tables = tables

        if self.conf['should_initialize_database']:
            self.__initiate_database()
        if show_tables:
            logger.info(self._get_all_tables())

    def _conn_singleton(self) -> Connection:
        self.conn = ""
        conf = self.conf
        try:
            self.conn = connect(
                host=conf['host'],
                dbname=conf['dbname'],
                user=conf['user'],
                password=conf['password'])
        except errors.ConnectionDoesNotExist as e:
            logger.exception(f'db connect failed {conf}')
            raise e
        except errors.OperationalError as e:
            logger.exception(f'db connect failed {conf}')
            raise e
        return self.conn

    def __initiate_database(self) -> None:
        """
        Database initialization, add the tables or drop it.
        """
        with self._conn_singleton() as conn:
            logger.info("Connecting to DB")
            with conn.cursor() as cur:  # get the cursor
                for dict in self.tables:
                    exists = self.__exists_check(dict)

                    for key, value in dict.items():
                        if exists:
                            logger.info(f"This table {key} already exists.")
                        else:
                            cur.execute(value)
                            logger.info(f"Added {key} table to the DB.")

    def __exists_check(self, table: dict[str, str]) -> bool:
        """
            Args:
                table: dict[str, str]:  Dict(key-> name of the table, value-> "table").
            Returns:
                A Boolean, if it is exist true, if it is not then false.
        """

        with self._conn_singleton() as conn:
            with conn.cursor() as cur:
                name = self.__get_table_name(table)

                cur.execute("""
                SELECT EXISTS(
                SELECT FROM
                    pg_tables
                WHERE 
                     schemaname = 'public' AND
                     tablename = (%(name)s)
                     )
                    """, {"name": str(name).lower()}
                        )
                exists = cur.fetchone()
                return exists[0]

    def _get_all_tables(self) -> List:
        """
            Get all of the tables in the DB.
        """
        with self._conn_singleton() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        *
                    FROM
                    information_schema.tables
                """)
                return cur.fetchall()

    # noinspection PyMethodMayBeStatic
    def __get_table_name(self, table: dict[str, str]) -> str:
        """
            ARGS:
                table: dict[str, str]:dict(key-> name of the table, value-> "table").
            RETURNS:
                str: The Name of the table
        """

        for key, value in table.items():
            return str(key)

    def handle_slorm(self):
        pass


api = SlobyDB()