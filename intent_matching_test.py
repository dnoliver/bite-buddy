import unittest

from intent_matching import IntentMatching


class TestIntentMatching(unittest.TestCase):
    def setUp(self):
        self.intent_matching = IntentMatching()

    def test_intent_matching(self):
        test_utterances = [
            ("I see apples and oranges in the pantry", "InventoryEntryIntent"),
            ("List everything I have in my fridge", "InventoryQueryIntent"),
            ("Remove the milk from my inventory", "InventoryDeleteIntent"),
            ("Show the items in my pantry", "InventoryQueryIntent"),
            ("Forget what I have in my fridge", "InventoryDeleteIntent"),
            ("I've got rice stored in the cabinets", "InventoryEntryIntent"),
            ("Enumerate the products in my pantry", "InventoryQueryIntent"),
            ("Forget what I have in my freezer", "InventoryDeleteIntent"),
            ("There's cheese sitting in the fridge", "InventoryEntryIntent"),
            ("Show the items in my kitchen's shelf", "InventoryQueryIntent"),
        ]

        for utterance, expected_intent in test_utterances:
            with self.subTest(utterance=utterance, expected_intent=expected_intent):
                result = self.intent_matching.run(utterance)
                self.assertIn(expected_intent, result)


if __name__ == "__main__":
    unittest.main()
