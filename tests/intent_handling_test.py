import os
import unittest

from src.database import Database
from src.intent_handling import (
    InventoryDeleteIntentHandling,
    InventoryEntryIntentHandling,
    InventoryQueryIntentHandling,
    ProductQueryIntentHandling,
    RecipeQueryIntentHandling,
)


class TestInventoryQueryIntentHandling(unittest.TestCase):
    def setUp(self):
        # Create a new database in memory
        self.database = Database(":memory:")

        # Initialize intent handling class
        self.intent_handling = InventoryQueryIntentHandling(database=self.database)

        # Add Mock Data
        self.database.insert_product_in_location("fridge", "tomatoes")
        self.database.insert_product_in_location("fridge", "bananas")
        self.database.insert_product_in_location("pantry", "tomatoes")

    def tearDown(self):
        self.database.close_connection()

    def test_intent_handling(self):
        test_utterances = [
            (
                "List everything I have in my fridge",
                "In the kitchen's fridge you have: tomatoes, bananas.",
            ),
            (
                "Enumerate the products in my pantry",
                "In the kitchen's pantry you have: tomatoes.",
            ),
            (
                "Show the items in my kitchen's shelf",
                "There are no products in the kitchen's shelf.",
            ),
        ]

        for utterance, expected_intent in test_utterances:
            with self.subTest(utterance=utterance, expected_intent=expected_intent):
                result = self.intent_handling.run(utterance)
                self.assertIn(expected_intent, result)


class TestInventoryEntryIntentHandling(unittest.TestCase):
    def setUp(self):
        # Create a new database in memory
        self.database = Database(":memory:")

        # Initialize intent handling class
        self.intent_handling = InventoryEntryIntentHandling(database=self.database)

        # Add Mock Data
        self.database.insert_product_in_location("fridge", "tomatoes")
        self.database.insert_product_in_location("fridge", "bananas")
        self.database.insert_product_in_location("pantry", "tomatoes")

    def tearDown(self):
        self.database.close_connection()

    def test_inventory_entry_intent_handling(self):
        test_utterances = [
            (
                "Add apples and oranges to my fridge",
                "Ok, I got apples, oranges in the fridge.",
            ),
            (
                "Add apples to my pantry",
                "Ok, I got apples in the pantry.",
            ),
            (
                "Add bananas and milk to my kitchen's shelf",
                "Ok, I got bananas, milk in the shelf.",
            ),
        ]

        for utterance, expected_intent in test_utterances:
            with self.subTest(utterance=utterance, expected_intent=expected_intent):
                result = self.intent_handling.run(utterance)
                self.assertIn(expected_intent, result)


class TestInventoryDeleteIntentHandling(unittest.TestCase):
    def setUp(self):
        # Create a new database in memory
        self.database = Database(":memory:")

        # Initialize intent handling class
        self.intent_handling = InventoryDeleteIntentHandling(database=self.database)

        # Add Mock Data
        self.database.insert_product_in_location("fridge", "tomatoes")
        self.database.insert_product_in_location("fridge", "bananas")
        self.database.insert_product_in_location("pantry", "tomatoes")

    def tearDown(self):
        self.database.close_connection()

    def test_inventory_delete_intent_handling(self):
        test_utterances = [
            (
                "Remove everything from my fridge",
                "Ok, I cleared the kitchen's fridge.",
            ),
            (
                "Clear my pantry",
                "Ok, I cleared the kitchen's pantry.",
            ),
            (
                "Delete all items from my kitchen's shelf",
                "Ok, I cleared the kitchen's shelf.",
            ),
        ]

        for utterance, expected_intent in test_utterances:
            with self.subTest(utterance=utterance, expected_intent=expected_intent):
                result = self.intent_handling.run(utterance)
                self.assertIn(expected_intent, result)


class TestProductQueryIntentHandling(unittest.TestCase):
    def setUp(self):
        # Create a new database in memory
        self.database = Database(":memory:")

        # Initialize intent handling class
        self.intent_handling = ProductQueryIntentHandling(database=self.database)

        # Add Mock Data
        self.database.insert_product_in_location("fridge", "tomatoes")
        self.database.insert_product_in_location("fridge", "bananas")
        self.database.insert_product_in_location("pantry", "tomatoes")

    def tearDown(self):
        self.database.close_connection()

    def test_product_query_intent_handling(self):
        test_utterances = [
            (
                "Where is the milk",
                "You don't have milk.",
            ),
            (
                "Find the bananas",
                "You have bananas in the fridge.",
            ),
            (
                "Help me find the tomatoes",
                "You have tomatoes in multiple locations: fridge, pantry.",
            ),
        ]

        for utterance, expected_intent in test_utterances:
            with self.subTest(utterance=utterance, expected_intent=expected_intent):
                result = self.intent_handling.run(utterance)
                self.assertIn(expected_intent, result)


class TestRecipeQueryIntentHandling(unittest.TestCase):
    def setUp(self):
        # Create a new database in memory
        self.database = Database(":memory:")

        # Initialize intent handling class
        self.intent_handling = RecipeQueryIntentHandling(database=self.database)

        # Add Mock Data
        self.database.insert_product_in_location("fridge", "tomatoes")
        self.database.insert_product_in_location("fridge", "bananas")
        self.database.insert_product_in_location("pantry", "tomatoes")

    def tearDown(self):
        self.database.close_connection()

    def test_product_query_intent_handling(self):
        utterance = "Give me a recipe"
        result = self.intent_handling.run(utterance)

        self.assertIn("Here is a recipe for you:", result)


if __name__ == "__main__":
    unittest.main()
