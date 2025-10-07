import random
from Entities.Farm_Object import Wheat, Corn, Chicken, Cow
from Entities.Utils import SEPARATOR_LENGTH, print_separator

class Market:
    def __init__(self):
        # type, price, sell_price, class
        self.plant_details = {
            "Wheat": ("plant", 10, 20, Wheat),
            "Corn": ("plant", 15, 25, Corn),
        }
        self.animal_details = {
            "Chicken": ("animal", 25, 15, Chicken),
            "Cow": ("animal", 40, 25, Cow),
        }

        self.all_details = {**self.plant_details, **self.animal_details}
        self.stock = {}

    def generate_stock(self):
        # Generates random stock for purchase each day
        self.stock = {}

        all_plants = list(self.plant_details.keys())
        num_to_choose = random.randint(1, len(all_plants))
        plant_names = random.sample(all_plants, num_to_choose)
        for name in plant_names:
            t, price, sell_price, cls = self.plant_details[name]
            obj = cls()
            qty = random.randint(2, 5)
            self.stock[name] = (t, obj.max_growth, obj.size, price, sell_price, obj.product_exp, qty)

        all_animals = list(self.animal_details.keys())
        num_to_choose = random.randint(1, len(all_animals))
        animal_names = random.sample(all_animals, num_to_choose)
        for name in animal_names:
            t, price, sell_price, cls = self.animal_details[name]
            obj = cls()
            qty = random.randint(1, 3)
            self.stock[name] = (t, obj.max_growth, obj.size, price, sell_price, obj.product_exp, qty)

    def show_stock(self):
        print("\n" + "=" * SEPARATOR_LENGTH)
        print("🏪 BUY STOCK (Seeds & Animals)")
        print_separator()

        if not self.stock:
            print(" - Closed today.")
        else:
            for name, info in self.stock.items():
                t, mg, size, price, sell_price, exp, qty = info
                icon = "🌱" if t == "plant" else "🐄"
                item_label = f"{icon} {name} ({size} slot)"
                print(f"  {item_label:<20}: ${price} ({qty} in stock)")

        print("\n" + "-" * SEPARATOR_LENGTH)
        print("📈 SELL PRICES (Products)")
        print_separator()

        sellable_products = {
            "Wheat": self.plant_details["Wheat"][2],
            "Corn": self.plant_details["Corn"][2],
            "Egg": self.animal_details["Chicken"][2],
            "Milk": self.animal_details["Cow"][2],
        }

        for prod, price in sellable_products.items():
            print(f"  {prod:<12}: ${price}")
        print("-" * SEPARATOR_LENGTH)

    def buy(self, player, farm, item_name_input, quantity):
        item_name = None
        for key in self.stock:
            if key.lower() == item_name_input.lower():
                item_name = key
                break

        if not item_name:
            print("⚠️ Item not available in today's market.")
            return

        t, mg, size, price, sell_price, exp, qty_stock = self.stock[item_name]
        total_cost = price * quantity
        total_size = size * quantity

        if quantity <= 0:
            print("❌ Quantity must be greater than 0.")
            return
        if quantity > qty_stock:
            print(f"❌ Insufficient stock! Available: {qty_stock} for {item_name}.")
            return
        if player.money < total_cost:
            print(f"💸 Insufficient money! Need ${total_cost}, you have ${player.money}.")
            return
        if farm.current_used + total_size > player.farm_size:
            remaining_slots = player.farm_size - farm.current_used
            print(f"⚠️ Insufficient Farm slots! Remaining: {remaining_slots} slots, need {total_size} slots.")
            return

        player.change_money(-total_cost)

        Object_Class = self.all_details[item_name][-1]
        for _ in range(quantity):
            obj = Object_Class()
            farm.objects.append(obj)
            farm.current_used += obj.size

        self.stock[item_name] = (t, mg, size, price, sell_price, exp, qty_stock - quantity)
        print(f"🛒 You bought {quantity}x {item_name} for ${total_cost} and placed it on the farm!")

    def sell(self, player, item_name_input, quantity_str):
        sellable_products = {
            "Wheat": self.plant_details["Wheat"][2],
            "Corn": self.plant_details["Corn"][2],
            "Egg": self.animal_details["Chicken"][2],
            "Milk": self.animal_details["Cow"][2],
        }

        item_name = None
        for key in sellable_products:
            if key.lower() == item_name_input.lower():
                item_name = key
                break

        if not item_name:
            print("⚠️ That item is not a sellable product.")
            return

        try:
            quantity = int(quantity_str)
        except ValueError:
            print("❌ Invalid quantity.")
            return

        if quantity <= 0:
            print("❌ Quantity must be positive.")
            return

        price = sellable_products[item_name]
        if player.inventory.remove_item(item_name, quantity):
            total = price * quantity
            player.change_money(total)
            print(f"💰 Sold {quantity}x {item_name} for ${total}!")
