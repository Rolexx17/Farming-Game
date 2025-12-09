from abc import ABC, abstractmethod

class FarmObject(ABC):
    def __init__(self, name, max_growth, size, product_name, product_exp):
        self._name = name
        self._growth = 1
        self._max_growth = max_growth
        self._size = size
        self._product_name = product_name
        self._product_exp = product_exp
        self._action_done_today = False

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size

    @property
    def product_name(self):
        return self._product_name

    @property
    def product_exp(self):
        return self._product_exp

    @property
    def growth(self):
        return self._growth

    @property
    def max_growth(self):
        return self._max_growth

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def harvestable_or_collectable(self):
        pass

    @abstractmethod
    def reset_after_collection(self):
        pass

    def reset_daily_status(self):
        self._action_done_today = False


class Plant(FarmObject):
    def action(self):
        if self._action_done_today:
            print(f"💧 {self.name} already watered today!")
            return False
        if self._growth < self._max_growth:
            self._growth += 1
            self._action_done_today = True
            print(f"💧 You watered {self.name}! +1 growth ({self._growth}/{self._max_growth})")
            return True
        print(f"✅ {self.name} is already fully grown.")
        return False

    def harvestable_or_collectable(self):
        return self._growth >= self._max_growth

    def reset_after_collection(self):
        # Plants are removed upon collection (handled by Farm)
        pass

    def check_daily_neglect(self):
        if not self._action_done_today and not self.harvestable_or_collectable():
            self._growth -= 1
            if self._growth <= -1:
                print(f"💀 Plant death: {self.name} died from neglect!")
                return True
            print(f"🍂 Neglect: {self.name} was not watered and lost 1 growth ({self._growth}/{self._max_growth}).")
        return False


class Wheat(Plant):
    def __init__(self):
        super().__init__("Wheat", 3, 1, "Wheat", 5)


class Corn(Plant):
    def __init__(self):
        super().__init__("Corn", 4, 2, "Corn", 8)


class Animal(FarmObject):
    def action(self):
        if self._action_done_today:
            print(f"🥕 {self.name} already fed today!")
            return False
        if self._growth < self._max_growth:
            self._growth += 1
            self._action_done_today = True
            print(f"🥕 You fed {self.name}! +1 production growth ({self._growth}/{self._max_growth})")
            return True
        print(f"🐄 {self.name} is ready to produce!")
        return False

    def harvestable_or_collectable(self):
        return self._growth >= self._max_growth

    def reset_after_collection(self):
        self._growth = 1
        self._action_done_today = False

    def check_daily_neglect(self):
        if not self._action_done_today and not self.harvestable_or_collectable():
            self._growth -= 1
            if self._growth <= -1:
                print(f"💀 Animal death: {self.name} died from neglect!")
                return True
            print(f"🦴 Neglect: {self.name} was not fed and lost 1 production growth ({self._growth}/{self._max_growth}).")
        return False


class Chicken(Animal):
    def __init__(self):
        super().__init__("Chicken", 3, 2, "Egg", 8)


class Cow(Animal):
    def __init__(self):
        super().__init__("Cow", 5, 3, "Milk", 12)
