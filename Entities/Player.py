from abc import ABC, abstractmethod, abstractproperty
from Entities.Inventory import Inventory

class Player:
    def __init__(self, name):
        self._name = name
        self._level = 1
        self._exp = 0
        self._money = 120
        self.inventory = Inventory()
        self._farm_size = 10
        self.inventory.add_item("Wheat", 5)

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def money(self):
        return self._money

    @property
    def exp(self):
        return self._exp

    @property
    def farm_size(self):
        return self._farm_size

    def change_money(self, amount):
        self._money += amount

    def add_exp(self, amount):
        self._exp += amount
        required_exp = self._level * 20
        if self._exp >= required_exp:
            self._exp -= required_exp
            self._level += 1
            self._farm_size += 5
            self.inventory.max_capacity += 5
            print(f"\n🌟 LEVEL UP! You reached Level {self._level}!")
            print(f"➡️ Farm size increased to {self._farm_size} and inventory capacity to {self.inventory.max_capacity}!\n")