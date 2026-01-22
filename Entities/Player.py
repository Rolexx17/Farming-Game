from Entities.Inventory import Inventory

class Player:
    def __init__(self, name):
        self.name, self.level, self.exp, self.money = name, 1, 0, 120
        self.farm_size = 10
        self.inventory = Inventory()
        self.inventory.add_item("Wheat", 5)

    def change_money(self, amount): self.money += amount
    def add_exp(self, amount):
        self.exp += amount
        req = self.level * 20
        if self.exp >= req:
            self.exp -= req
            self.level += 1
            self.farm_size += 5
            self.inventory.max_capacity += 5
            print(f"\n🌟 LEVEL UP! Now Level {self.level}")