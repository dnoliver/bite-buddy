import unittest

from intent_handling import (
    InventoryDeleteIntentHandling,
    InventoryEntryIntentHandling,
    InventoryQueryIntentHandling,
)


class TestIntentMatching(unittest.TestCase):
    def setUp(self):
        self.inventory_query_intent_handling = InventoryQueryIntentHandling()
        self.inventory_entry_intent_handling = InventoryEntryIntentHandling()
        self.inventory_delete_intent_handling = InventoryDeleteIntentHandling()

    def test_inventory_query_intent_handling(self):
        test_utterances = [
            (
                "List everything I have in my fridge",
                "In the kitchen's fridge you have: tomatoes, bananas.",
            ),
            (
                "Show the items in my pantry",
                "In the kitchen's pantry you have: tomatoes, bananas.",
            ),
            (
                "Enumerate the products in my pantry",
                "In the kitchen's pantry you have: tomatoes, bananas.",
            ),
            (
                "Show the items in my kitchen's shelf",
                "In the kitchen's shelf you have: tomatoes, bananas.",
            ),
        ]

        for utterance, expected_intent in test_utterances:
            with self.subTest(utterance=utterance, expected_intent=expected_intent):
                result = self.inventory_query_intent_handling.run(utterance)
                self.assertIn(expected_intent, result)

    def test_inventory_entry_intent_handling(self):
        test_utterances = [
            (
                "Add apples and oranges to my fridge",
                "Ok, I got apples, oranges in the fridge.",
            ),
            (
                "Add apples and oranges to my pantry",
                "Ok, I got apples, oranges in the pantry.",
            ),
            (
                "Add apples and oranges to my kitchen's shelf",
                "Ok, I got apples, oranges in the shelf.",
            ),
        ]

        for utterance, expected_intent in test_utterances:
            with self.subTest(utterance=utterance, expected_intent=expected_intent):
                result = self.inventory_entry_intent_handling.run(utterance)
                self.assertIn(expected_intent, result)

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
                result = self.inventory_delete_intent_handling.run(utterance)
                self.assertIn(expected_intent, result)


if __name__ == "__main__":
    unittest.main()
