from slot_parsing import (
    LocationInKitchenSlotParsing,
    ProductListSlotParsing,
    ProductQuantitySlotParsing,
)


class InventoryQueryIntentHandling:

    def __init__(self):
        self.location_in_kitchen_parser = LocationInKitchenSlotParsing()

    def run(self, utterance: str):
        location_in_kitchen = self.location_in_kitchen_parser.run(utterance)

        return f"In the kitchen's {location_in_kitchen} you have: tomatoes, bananas."


class InventoryEntryIntentHandling:

    def __init__(self):
        self.location_in_kitchen_parser = LocationInKitchenSlotParsing()
        self.product_list_parser = ProductListSlotParsing()

    def run(self, utterance: str):
        location_in_kitchen = self.location_in_kitchen_parser.run(utterance)
        product_list = self.product_list_parser.run(utterance)

        return f"Ok, I got {product_list} in the {location_in_kitchen}."


class InventoryDeleteIntentHandling:

    def __init__(self):
        self.location_in_kitchen_parser = LocationInKitchenSlotParsing()

    def run(self, utterance: str):
        location_in_kitchen = self.location_in_kitchen_parser.run(utterance)

        return f"Ok, I cleared the kitchen's {location_in_kitchen}."
