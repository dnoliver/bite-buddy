import unittest

from intent_matching import IntentMatching


class TestIntentMatching(unittest.TestCase):
    def setUp(self):
        self.intent_matching = IntentMatching()

    def test_intent_matching(self):
        test_utterances = [
            # Inventory Entry Intent
            ("I see apples and oranges in the pantry", "InventoryEntryIntent"),
            ("I've got rice stored in the cabinets", "InventoryEntryIntent"),
            ("There's cheese sitting in the fridge", "InventoryEntryIntent"),
            # Inventory Query Intent
            ("List everything I have in my fridge", "InventoryQueryIntent"),
            ("Enumerate the products in my pantry", "InventoryQueryIntent"),
            ("Show the items in my pantry", "InventoryQueryIntent"),
            # Inventory Delete Intent
            ("Remove the milk from my inventory", "InventoryDeleteIntent"),
            ("Forget what I have in my fridge", "InventoryDeleteIntent"),
            ("Forget what I have in my freezer", "InventoryDeleteIntent"),
            # Product Query Intent
            ("Where is the milk", "ProductQueryIntent"),
            ("Find the tomatoes", "ProductQueryIntent"),
            ("Help me find the sugar", "ProductQueryIntent"),
        ]

        for utterance, expected_intent in test_utterances:
            with self.subTest(utterance=utterance, expected_intent=expected_intent):
                result = self.intent_matching.run(utterance)
                self.assertIn(expected_intent, result)


if __name__ == "__main__":
    unittest.main()
