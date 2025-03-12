from haystack import Document, Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import OpenAIGenerator

from src.database import Database
from src.slot_parsing import (
    LocationInKitchenSlotParsing,
    ProductListSlotParsing,
    ProductQuantitySlotParsing,
)


class InventoryQueryIntentHandling:

    def __init__(self, database: Database):
        self.location_in_kitchen_parser = LocationInKitchenSlotParsing()
        self.database = database

    def run(self, utterance: str):
        location_in_kitchen = self.location_in_kitchen_parser.run(utterance)

        if location_in_kitchen == "kitchen":
            products = self.database.list_products()
        else:
            products = self.database.list_products_by_location(location_in_kitchen)

        if len(products) == 0:
            return f"There are no products in the kitchen's {location_in_kitchen}."

        if location_in_kitchen == "kitchen":
            return f"In the kitchen you have: {', '.join(products)}."
        else:
            return f"In the kitchen's {location_in_kitchen} you have: {', '.join(products)}."


class InventoryEntryIntentHandling:

    def __init__(self, database: Database):
        self.location_in_kitchen_parser = LocationInKitchenSlotParsing()
        self.product_list_parser = ProductListSlotParsing()
        self.database = database

    def run(self, utterance: str):
        location_in_kitchen = self.location_in_kitchen_parser.run(utterance)
        product_list = self.product_list_parser.run(utterance).split(", ")
        for product in product_list:
            self.database.insert_product_in_location(location_in_kitchen, product)

        return f"Ok, I got {(", ").join(product_list)} in the {location_in_kitchen}."


class InventoryDeleteIntentHandling:

    def __init__(self, database: Database):
        self.location_in_kitchen_parser = LocationInKitchenSlotParsing()
        self.database = database

    def run(self, utterance: str):
        location_in_kitchen = self.location_in_kitchen_parser.run(utterance)
        self.database.delete_products_by_location(location_in_kitchen)

        return f"Ok, I cleared the kitchen's {location_in_kitchen}."


class ProductQueryIntentHandling:

    def __init__(self, database: Database):
        self.product_list_parser = ProductListSlotParsing()
        self.database = database

    def run(self, utterance: str):
        product_list = self.product_list_parser.run(utterance).split(", ")
        locations = self.database.find_product(product_list[0])

        if len(locations) == 0:
            return f"You don't have {product_list[0]}."
        if len(locations) == 1:
            return f"You have {product_list[0]} in the {locations[0]}."
        if len(locations) > 1:
            return f"You have {product_list[0]} in multiple locations: {', '.join(locations)}."


class RecipeQueryIntentHandling:

    def __init__(self, database: Database):
        self.database = database

        self.pipeline = Pipeline()

        with open("prompts/recipe-query.txt") as f:
            self.prompt_template = f.read()

        self.pipeline.add_component(
            instance=PromptBuilder(template=self.prompt_template), name="prompt_builder"
        )
        self.pipeline.add_component(instance=OpenAIGenerator(), name="llm")
        self.pipeline.connect("prompt_builder", "llm")

    def run(self, utterance: str):
        product_list = self.database.list_products()

        if len(product_list) == 0:
            return "You don't have any products in the kitchen."

        documents = []
        for product in product_list:
            documents.append(Document(content=product))
        result = self.pipeline.run({"prompt_builder": {"documents": documents}})
        return result["llm"]["replies"][0]
