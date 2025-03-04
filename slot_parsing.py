from haystack import Pipeline, Document
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
import unittest
from dotenv import load_dotenv
from pathlib import Path

from haystack.components.converters import TextFileToDocument

load_dotenv(dotenv_path=Path(".") / ".env")


class SlotParsing:

    slot_path = None
    prompt_path = None

    def __init__(self):

        if not self.slot_path:
            raise ValueError("slot_path cannot be None")

        if not self.prompt_path:
            raise ValueError("prompt_path cannot be None")

        converter = TextFileToDocument()
        self.documents = converter.run(
            sources=[
                Path(self.slot_path),
            ]
        )["documents"]

        with open(self.prompt_path) as f:
            self.prompt_template = f.read()

        self.pipeline = Pipeline()
        self.pipeline.add_component(
            instance=PromptBuilder(template=self.prompt_template), name="prompt_builder"
        )
        self.pipeline.add_component(instance=OpenAIGenerator(), name="llm")
        self.pipeline.connect("prompt_builder", "llm")

    def run(self, utterance: str):
        result = self.pipeline.run(
            {
                "prompt_builder": {
                    "documents": self.documents,
                    "query": utterance,
                }
            }
        )

        return result["llm"]["replies"][0]


class LocationInKitchenSlotParsion(SlotParsing):
    slot_path = "slots/location-in-kitchen.yml"
    prompt_path = "prompts/slot-parsing.txt"


class ProductListSlotParsing(SlotParsing):
    slot_path = "slots/product-list.yml"
    prompt_path = "prompts/slot-parsing.txt"


class ProductQuantitySlotParsing(SlotParsing):
    slot_path = "slots/product-quantity.yml"
    prompt_path = "prompts/slot-parsing.txt"
