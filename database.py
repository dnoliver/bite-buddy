import logging
import sqlite3
from sqlite3 import Error

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    _instance = None

    def __new__(cls, db_file):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize(db_file)
        return cls._instance

    def _initialize(self, db_file):
        self.connection = self._create_connection(db_file)

        create_table_query = """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            product TEXT NOT NULL
        );
        """
        self.execute_query(create_table_query)

        create_trigger_query = """
        CREATE TRIGGER IF NOT EXISTS remove_duplicates
        AFTER INSERT ON inventory
        BEGIN
            DELETE FROM inventory
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM inventory
                GROUP BY location, product
            );
        END;
        """
        self.execute_query(create_trigger_query)

    def _create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file, check_same_thread=False)
            logger.info(f"Connected to SQLite database: {db_file}")
        except Error as e:
            logger.error(f"Error connecting to database: {e}")
        return conn

    def insert_product_in_location(self, location, product):
        insert_query = """
        INSERT INTO inventory (location, product)
        VALUES (?, ?);
        """
        self.execute_query(insert_query, (location, product))

    def list_products_by_location(self, location):
        select_query = """
        SELECT product FROM inventory
        WHERE location = ?;
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query, (location,))
            products = cursor.fetchall()
            return [product[0] for product in products]
        except Error as e:
            logger.error(f"Error fetching products: {e}")
            return []

    def delete_products_by_location(self, location):
        delete_query = """
        DELETE FROM inventory
        WHERE location = ?;
        """
        self.execute_query(delete_query, (location,))
    
    def find_product(self, product):
        select_query = """
        SELECT location FROM inventory
        WHERE product = ?;
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query, (product,))
            locations = cursor.fetchall()
            return [location[0] for location in locations]
        except Error as e:
            logger.error(f"Error fetching locations: {e}")
            return []

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            logger.info("Query executed successfully")
        except Error as e:
            logger.error(f"Error executing query: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            logger.info("Connection to SQLite database closed.")
