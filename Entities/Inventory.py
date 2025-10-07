from Entities.Utils import SEPARATOR_LENGTH, print_separator

class Inventory:
    def __init__(self):
        self.items = {} 
        self.max_capacity = 10

    def add_item(self, name, quantity=1):
        total_items = sum(self.items.values())
        if total_items + quantity > self.max_capacity:
            if quantity > 0:
                print(f"⚠️ Inventory full! ({total_items}/{self.max_capacity}). Could not add {name}.")
            return False
        self.items[name] = self.items.get(name, 0) + quantity
        return True

    def remove_item(self, name, quantity=1):
        if name in self.items and self.items[name] >= quantity:
            self.items[name] -= quantity
            if self.items[name] == 0:
                del self.items[name]
            return True
        print(f"⚠️ Not enough {name} in inventory.")
        return False

    def is_empty(self):
        return not bool(self.items)

    def show_inventory(self):
        print("\n" + "=" * SEPARATOR_LENGTH)
        print("🎒 INVENTORY")
        
        if not self.items:
            print_separator()
            print(" - Empty.")
        else:
            product_names = ["Wheat", "Corn", "Tomato", "Egg", "Milk"]
            items_list = list(self.items.items())
            sorted_items = []
            in_list = []
            not_in_list = []
            for item in items_list:
                key = item[0]
                value = item[1]
                if key in product_names:
                    in_list.append(item)
                else:
                    not_in_list.append(item)
            sorted_items = in_list + not_in_list

            print_separator()

            for item, qty in sorted_items:
                print(f"  {item:<15}: {qty} QTY")
                
        total_items = sum(self.items.values())
        print_separator()
        print(f"SLOTS USED: {total_items}/{self.max_capacity}")