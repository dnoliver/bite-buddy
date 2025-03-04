from haystack import Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
import unittest
from dotenv import load_dotenv
from pathlib import Path

from haystack.components.converters import TextFileToDocument

load_dotenv(dotenv_path=Path(".") / ".env")

converter = TextFileToDocument()
documents = converter.run(
    sources=[
        Path("intents/inventory-delete.yml"),
        Path("intents/inventory-entry.yml"),
        Path("intents/inventory-query.yml"),
    ]
)["documents"]

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
        p.add_component(
            instance=PromptBuilder(template=prompt_template), name="prompt_builder"
        )
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
            ("Show the items in my kitchen's shelf", "InventoryQueryIntent"),
        ]

        for utterance, expected_intent in test_utterances:
            with self.subTest(utterance=utterance, expected_intent=expected_intent):
                result = self.pipeline.run(
                    {
                        "prompt_builder": {
                            "documents": self.documents,
                            "query": utterance,
                        }
                    }
                )
                self.assertIn(expected_intent, result["llm"]["replies"][0])


if __name__ == "__main__":
    unittest.main()
