from database import Database
from slot_parsing import (
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
        products = self.database.list_products_by_location(location_in_kitchen)

        if len(products) == 0:
            return f"There are no products in the kitchen's {location_in_kitchen}."

        return (
            f"In the kitchen's {location_in_kitchen} you have: {', '.join(products)}."
        )


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
