from pathlib import Path

from dotenv import load_dotenv
from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.converters import TextFileToDocument
from haystack.components.generators import OpenAIGenerator

load_dotenv(dotenv_path=Path(".") / ".env")


class IntentMatching:

    def __init__(self):
        converter = TextFileToDocument()
        self.documents = converter.run(
            sources=[
                Path("intents/inventory-delete.yml"),
                Path("intents/inventory-entry.yml"),
                Path("intents/inventory-query.yml"),
            ]
        )["documents"]

        with open("prompts/intent-matching.txt") as f:
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
