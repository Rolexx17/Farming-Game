import unittest
from Entities.Farm_Object import Wheat, Chicken

class TestFarmObject(unittest.TestCase):

    def test_wheat_growth(self):
        w = Wheat()
        w.action()
        self.assertEqual(w.growth, 2)

    def test_harvestable(self):
        w = Wheat()
        for _ in range(3):
            w.action()
        self.assertTrue(w.harvestable_or_collectable())

    def test_animal_reset(self):
        c = Chicken()
        c._growth = c.max_growth
        c.reset_after_collection()
        self.assertEqual(c.growth, 1)

if __name__ == "__main__":
    unittest.main()
