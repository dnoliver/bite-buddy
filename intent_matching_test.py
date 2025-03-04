from haystack import Pipeline, Document
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
import unittest
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(".") / ".env")

intent_1 = Document(content="""
    Name: InventoryEntryIntent
    Description: This intent is used to add an item to the inventory.
    Training Phrases:
    - I see yogurt, beans, and tomatoes in the pantry
    - I've got pasta stored in the cabinets
    - There's tomatoes sitting in the fridge
    """)

intent_2 = Document(content="""
    Name: InventoryQueryIntent
    Description: This intent is used to query the inventory for a specific item.
    Training Phrases:
    - List everything I have in my freezer
    - Enumerate the products in my cabinets
    - Show the items in my kitchen's shelf
    """)

intent_3 = Document(content="""
    Name: InventoryDeleteIntent
    Description: This intent is used to remove an item from the inventory.
    Training Phrases:
    - Forget what I have in my kitchen
    - Forget what I have in my pantry
    - Remove the beans from my inventory
    """)

documents = [intent_1, intent_2, intent_3]

prompt_template = """
    You are a helpful assistant for a software engineer.
    The documents below describe Intents for a Voice Assistant application.
    Your objective is to classify the User Utterance, and reply with 
    the intent it is targeting. Just reply with the Name of the intent. \n
    Documents:
    {% for doc in documents %}
        {{ doc.content }}
    {% endfor %}

    User Utterance: {{query}}
    Target Intent:
    """

class TestIntentMatching(unittest.TestCase):
    def setUp(self):
        p = Pipeline()
        p.add_component(instance=PromptBuilder(template=prompt_template), name="prompt_builder")
        p.add_component(instance=OpenAIGenerator(), name="llm")
        p.connect("prompt_builder", "llm")

        self.pipeline = p
        self.documents = documents

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
            ("Show the items in my kitchen's shelf", "InventoryQueryIntent")
        ]

        for utterance, expected_intent in test_utterances:
            with self.subTest(utterance=utterance, expected_intent=expected_intent):
                result = self.pipeline.run({"prompt_builder": {"documents": self.documents, "query": utterance}})
                self.assertIn(expected_intent, result["llm"]["replies"][0])

if __name__ == "__main__":
    unittest.main()
