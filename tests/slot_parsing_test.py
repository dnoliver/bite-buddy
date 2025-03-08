import unittest

from src.slot_parsing import (
    LocationInKitchenSlotParsing,
    ProductListSlotParsing,
    ProductQuantitySlotParsing,
)


class TestSlotParsing(unittest.TestCase):
    def setUp(self):
        self.location_in_kitchen_slot_parsing = LocationInKitchenSlotParsing()
        self.product_list_slot_parsing = ProductListSlotParsing()
        self.product_quantity_slot_parsing = ProductQuantitySlotParsing()

    def test_location_in_kitchen_slot_parsing(self):
        test_utterances = [
            ("I see apples and oranges in the pantry", "pantry"),
            ("Remove the milk from my fridge", "fridge"),
            ("There's cheese sitting in the freezer", "freezer"),
            ("I've got pasta stored in the cabinets", "cabinets"),
            ("There's tomatoes and beans in the pantry", "pantry"),
            ("I see yogurt, beans, and tomatoes in the pantry", "pantry"),
            ("There's tomatoes sitting in the fridge", "fridge"),
            ("List the products in the kitchen", "kitchen"),
        ]

        for utterance, expected_slot_value in test_utterances:
            with self.subTest(
                utterance=utterance, expected_slot_value=expected_slot_value
            ):
                result = self.location_in_kitchen_slot_parsing.run(utterance)
                self.assertIn(expected_slot_value, result)

    def test_product_list_slot_parsing(self):
        test_utterances = [
            ("I see apples and oranges in the pantry", "apples, oranges"),
            ("Remove the milk from my fridge", "milk"),
            ("There's cheese sitting in the freezer", "cheese"),
            ("I've got pasta stored in the cabinets", "pasta"),
            ("There's tomatoes and beans in the pantry", "tomatoes, beans"),
            (
                "I see yogurt, beans, and tomatoes in the pantry",
                "yogurt, beans, tomatoes",
            ),
            ("There's tomatoes sitting in the fridge", "tomatoes"),
            ("In my pantry I have tomatoes and bananas", "tomatoes, bananas"),
        ]

        for utterance, expected_slot_value in test_utterances:
            with self.subTest(
                utterance=utterance, expected_slot_value=expected_slot_value
            ):
                result = self.product_list_slot_parsing.run(utterance)
                self.assertIn(expected_slot_value, result)

    def test_product_quantity_slot_parsing(self):
        test_utterances = [
            ("I have 3 gallons of milk in the fridge", "3 gallons"),
            ("I have 1 pound of cheese in the freezer", "1 pound"),
            ("I have 2 boxes of pasta in the cabinets", "2 boxes"),
        ]

        for utterance, expected_slot_value in test_utterances:
            with self.subTest(
                utterance=utterance, expected_slot_value=expected_slot_value
            ):
                result = self.product_quantity_slot_parsing.run(utterance)
                self.assertIn(expected_slot_value, result)


if __name__ == "__main__":
    unittest.main()
