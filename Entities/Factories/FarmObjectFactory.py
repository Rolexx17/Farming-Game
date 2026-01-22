from abc import ABC, abstractmethod
from Entities.Farm_Object import Wheat, Corn, Chicken, Cow

class FarmObjectFactory(ABC):
    @abstractmethod
    def create(self): pass


class WheatFactory(FarmObjectFactory):
    def create(self): return Wheat()


class CornFactory(FarmObjectFactory):
    def create(self): return Corn()


class ChickenFactory(FarmObjectFactory):
    def create(self): return Chicken()


class CowFactory(FarmObjectFactory):
    def create(self): return Cow()
