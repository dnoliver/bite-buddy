import os
import unittest

from src.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db = ":memory:"
        self.db = Database(self.test_db)
        self.db.execute_query("DELETE FROM inventory")  # Clear any existing data

    def tearDown(self):
        self.db.close_connection()

    def test_database(self):
        # Insert products into the database
        self.db.insert_product_in_location("pantry", "apples")
        self.db.insert_product_in_location("pantry", "oranges")
        self.db.insert_product_in_location("fridge", "milk")
        self.db.insert_product_in_location("freezer", "frozen peas")

        # Verify products are inserted
        products_in_pantry = self.db.list_products_by_location("pantry")
        self.assertIn("apples", products_in_pantry)
        self.assertIn("oranges", products_in_pantry)

        # Delete products by location
        self.db.delete_products_by_location("pantry")

        # Verify products are deleted
        products_in_pantry_after_delete = self.db.list_products_by_location("pantry")
        self.assertEqual(products_in_pantry_after_delete, [])

        # Verify products in other locations are not affected
        products_in_fridge = self.db.list_products_by_location("fridge")
        self.assertIn("milk", products_in_fridge)

        # Find products by name
        locations = self.db.find_product("milk")
        self.assertIn("fridge", locations)

        # List all products
        all_products = self.db.list_products()
        self.assertIn("milk", all_products)
        self.assertIn("frozen peas", all_products)


if __name__ == "__main__":
    unittest.main()
