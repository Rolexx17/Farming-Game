from Entities.Utils import print_separator, SEPARATOR_LENGTH

class Inventory:
    def __init__(self, capacity=10):
        self.items = {}
        self.max_capacity = capacity

    def add_item(self, name, quantity=1):
        if sum(self.items.values()) + quantity > self.max_capacity:
            return False
        self.items[name] = self.items.get(name, 0) + quantity
        return True

    def remove_item(self, name, quantity=1):
        if name in self.items and self.items[name] >= quantity:
            self.items[name] -= quantity
            if self.items[name] == 0: del self.items[name]
            return True
        return False

    def is_empty(self): return not bool(self.items)

    def show_inventory(self):
        print("\n" + "=" * SEPARATOR_LENGTH + "\n🎒 INVENTORY")
        print_separator()
        if not self.items:
            print(" - Empty.")
        else:
            for item, qty in self.items.items():
                print(f"  {item:<15}: {qty} QTY")
        print_separator()
        print(f"SLOTS USED: {sum(self.items.values())}/{self.max_capacity}")