import unittest

from src.intent_matching import IntentMatching


class BaseIntentMatchingTest:
    @staticmethod
    def setUp(self):
        self.intent_matching = IntentMatching()
        self.expected_intent = ""
        self.test_utterances = []

    @staticmethod
    def test_intent_matching(self):
        for utterance in self.test_utterances:
            with self.subTest(
                utterance=utterance, expected_intent=self.expected_intent
            ):
                result = self.intent_matching.run(utterance)
                self.assertIn(self.expected_intent, result)


class TestInventoryEntryIntentMatching(unittest.TestCase):
    def setUp(self):
        BaseIntentMatchingTest.setUp(self)
        self.expected_intent = "InventoryEntryIntent"
        self.test_utterances = [
            "I see apples and oranges in the pantry",
            "I've got rice stored in the cabinets",
            "There's cheese sitting in the fridge",
        ]

    def test_intent_matching(self):
        BaseIntentMatchingTest.test_intent_matching(self)


class TestInventoryQueryIntentMatching(unittest.TestCase):
    def setUp(self):
        BaseIntentMatchingTest.setUp(self)
        self.intent_matching = IntentMatching()
        self.expected_intent = "InventoryQueryIntent"
        self.test_utterances = [
            "List everything I have in my fridge",
            "Enumerate the products in my pantry",
            "Show the items in my pantry",
        ]

    def test_intent_matching(self):
        BaseIntentMatchingTest.test_intent_matching(self)


class TestInventoryDeleteIntentMatching(unittest.TestCase):
    def setUp(self):
        BaseIntentMatchingTest.setUp(self)
        self.expected_intent = "InventoryDeleteIntent"
        self.test_utterances = [
            "Remove the milk from my inventory",
            "Forget what I have in my fridge",
            "Forget what I have in my freezer",
        ]

    def test_intent_matching(self):
        BaseIntentMatchingTest.test_intent_matching(self)


class TestProductQueryIntentMatching(unittest.TestCase):
    def setUp(self):
        BaseIntentMatchingTest.setUp(self)
        self.expected_intent = "ProductQueryIntent"
        self.test_utterances = [
            "Where is the milk",
            "Find the tomatoes",
            "Help me find the sugar",
        ]

    def test_intent_matching(self):
        BaseIntentMatchingTest.test_intent_matching(self)


class TestRecipeQueryIntentMatching(unittest.TestCase):
    def setUp(self):
        BaseIntentMatchingTest.setUp(self)
        self.expected_intent = "RecipeQueryIntent"
        self.test_utterances = [
            "What can I make the products in my kitchen?",
            "Find a recipe for the products in my kitchen",
            "I need a recipe",
        ]

    def test_intent_matching(self):
        BaseIntentMatchingTest.test_intent_matching(self)


if __name__ == "__main__":
    unittest.main()
