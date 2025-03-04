from haystack import Pipeline, Document
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
import unittest
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(".") / ".env")

slot_1 = Document(content="""
    Name: LocationInKitchenSlot
    Description: This slot is used to capture the location of an item in the kitchen.
    Examples:
    - pantry
    - cabinets
    - fridge
    """)

slot_2 = Document(content="""
    Name: ProductListSlot
    Description: This slot is used to capture a list of products.
    Examples:
    - yogurt, beans, tomatoes
    - pasta, tomatoes
    - cheese, milk
    """)

slot_3 = Document(content="""
    Name: ProductQuantitySlot
    Description: This slot is used to capture the quantity of a product.
    Examples:
    - 3 gallons
    - 1 pound
    - 2 boxes
    """)

documents = [slot_1, slot_2, slot_3]

prompt_template = """
    You are a helful assistant for a software engineer.
    The documents below describe an Slot for a Voice Assistant application.
    Your objective is to extract the Slot from the User Utterance, and reply with
    the extracted value. Just reply with the value of the Slot. \n
    Documents:
    {% for doc in documents %}
        {{ doc.content }}
    {% endfor %}

    User Utterance: {{query}}
    Slot Value: 
    """

class TestSlotParsing(unittest.TestCase):
    def setUp(self):
        p = Pipeline()
        p.add_component(instance=PromptBuilder(template=prompt_template), name="prompt_builder")
        p.add_component(instance=OpenAIGenerator(), name="llm")
        p.connect("prompt_builder", "llm")

        self.pipeline = p
        self.documents = documents

    def test_location_in_kitchen_slot_parsing(self):
        test_utterances = [
            ("I see apples and oranges in the pantry", "pantry"),
            ("Remove the milk from my fridge", "fridge"),
            ("There's cheese sitting in the freezer", "freezer"),
            ("I've got pasta stored in the cabinets", "cabinets"),
            ("There's tomatoes and beans in the pantry", "pantry"),
            ("I see yogurt, beans, and tomatoes in the pantry", "pantry"),
            ("There's tomatoes sitting in the fridge", "fridge"),
        ]

        for utterance, expected_slot_value in test_utterances:
            with self.subTest(utterance=utterance, expected_slot_value=expected_slot_value):
                result = self.pipeline.run({"prompt_builder": {"documents": [self.documents[0]], "query": utterance}})
                self.assertIn(expected_slot_value, result["llm"]["replies"][0])

    def test_product_list_slot_parsing(self):
        test_utterances = [
            ("I see apples and oranges in the pantry", "apples, oranges"),
            ("Remove the milk from my fridge", "milk"),
            ("There's cheese sitting in the freezer", "cheese"),
            ("I've got pasta stored in the cabinets", "pasta"),
            ("There's tomatoes and beans in the pantry", "tomatoes, beans"),
            ("I see yogurt, beans, and tomatoes in the pantry", "yogurt, beans, tomatoes"),
            ("There's tomatoes sitting in the fridge", "tomatoes"),
        ]

        for utterance, expected_slot_value in test_utterances:
            with self.subTest(utterance=utterance, expected_slot_value=expected_slot_value):
                result = self.pipeline.run({"prompt_builder": {"documents": [self.documents[1]], "query": utterance}})
                self.assertIn(expected_slot_value, result["llm"]["replies"][0])

    def test_product_quantity_slot_parsing(self):
        test_utterances = [
            ("I have 3 gallons of milk in the fridge", "3 gallons"),
            ("I have 1 pound of cheese in the freezer", "1 pound"),
            ("I have 2 boxes of pasta in the cabinets", "2 boxes"),
        ]

        for utterance, expected_slot_value in test_utterances:
            with self.subTest(utterance=utterance, expected_slot_value=expected_slot_value):
                result = self.pipeline.run({"prompt_builder": {"documents": [self.documents[2]], "query": utterance}})
                self.assertIn(expected_slot_value, result["llm"]["replies"][0])

if __name__ == "__main__":
    unittest.main()
