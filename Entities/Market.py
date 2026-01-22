import random
from abc import ABC, abstractmethod
from Entities.Utils import SEPARATOR_LENGTH, print_separator
from Entities.Factories.FarmObjectFactory import (
    WheatFactory, CornFactory, ChickenFactory, CowFactory
)

class PricingStrategy(ABC):
    @abstractmethod
    def get_buy_price(self, base_price): pass
    @abstractmethod
    def get_sell_price(self, base_price): pass


class NormalPricing(PricingStrategy):
    def get_buy_price(self, base_price): return base_price
    def get_sell_price(self, base_price): return base_price


class Market:
    def __init__(self):
        self.pricing_strategy = NormalPricing()
        self.factories = {
            "Wheat": WheatFactory(),
            "Corn": CornFactory(),
            "Chicken": ChickenFactory(),
            "Cow": CowFactory()
        }

        self.stock = {
            "Wheat": (10, 20, 2, 5),
            "Corn": (15, 25, 2, 5),
            "Chicken": (25, 15, 1, 3),
            "Cow": (40, 25, 1, 3)
        }

    def generate_stock(self): pass

    def show_stock(self):
        print("\n" + "=" * SEPARATOR_LENGTH)
        print("🏪 BUY STOCK (Seeds & Animals)")
        print_separator()
        for k, v in self.stock.items():
            print(f"  {k:<10}: ${v[0]}")
        print("-" * SEPARATOR_LENGTH)

    def buy(self, player, farm, item_name_input, qty):
        item_name = None
        for key in self.factories:
            if key.lower() == item_name_input.lower():
                item_name = key
                break

        if not item_name:
            print("⚠️ Item not available.")
            return

        factory = self.factories[item_name]
        price = self.stock[item_name][0]
        total = price * qty

        if player.money < total:
            print("💸 Insufficient money!")
            return

        player.change_money(-total)
        for _ in range(qty):
            obj = factory.create()
            farm.objects.append(obj)
            farm.current_used += obj.size

        print(f"🛒 You bought {qty}x {item_name} for ${total}!")
    
    def sell(self, player, item_name_input, quantity):
        sellable_products = {
            "Wheat": 20,
            "Corn": 25,
            "Egg": 15,
            "Milk": 25
        }

        item_name = None
        for key in sellable_products:
            if key.lower() == item_name_input.lower():
                item_name = key
                break

        if not item_name:
            print("⚠️ That item is not a sellable product.")
            return

        if quantity <= 0:
            print("❌ Quantity must be positive.")
            return

        if item_name not in player.inventory.items:
            print(f"⚠️ You don't have any {item_name} to sell.")
            return

        if player.inventory.items[item_name] < quantity:
            print(f"⚠️ Not enough {item_name} to sell. You have {player.inventory.items[item_name]}.")
            return

        price = sellable_products[item_name]
        player.inventory.remove_item(item_name, quantity)
        total = price * quantity
        player.change_money(total)
        print(f"💰 Sold {quantity}x {item_name} for ${total}!")

