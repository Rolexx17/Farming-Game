import sys
import asyncio
from abc import ABC, abstractmethod
from Entities.Utils import clear, print_title, print_separator, SEPARATOR_LENGTH, WAKE_UP_HOUR, BED_TIME
from Entities.Player import Player
from Entities.Market import Market
from Entities.Farm import Farm
from Entities.Farm_Object import Plant, Animal, Wheat, Corn, Chicken, Cow

class GameFacade:
    def __init__(self, player: Player, market: Market, farm: Farm):
        self.player = player
        self.market = market
        self.farm = farm

    def show_status(self, day, hour):
        status_line = f"🧑‍🌾 FARMER: {self.player.name.upper()} | ⭐ LV: {self.player.level} | 💰 MONEY: ${self.player.money} | 🗓️ DAY: {day} | ⏰ TIME: {hour:02d}:00 | 📈 EXP: {self.player.exp}/{self.player.level * 20}"
        print("=" * 80)
        print(status_line)
        print("=" * 80)

    def buy_item(self, item, qty):
        self.market.buy(self.player, self.farm, item, qty)

    def sell_item(self, item, qty):
        self.market.sell(self.player, item, qty)

    def show_market(self):
        self.market.show_stock()

    def show_inventory(self):
        self.player.inventory.show_inventory()

    def harvest_collect_all(self):
        return self.farm.harvest_collect_all(self.player)

    def perform_actions(self, indices_str, action_type):
        return self.farm.perform_action_on_selected(indices_str, action_type)


class GameState(ABC):
    def __init__(self, game):
        self.game = game

    @property
    @abstractmethod
    def can_act(self):
        pass

    @abstractmethod
    def check_transition(self):
        pass


class DayState(GameState):
    @property
    def can_act(self):
        return True

    def check_transition(self):
        if self.game.hour >= BED_TIME:
            self.game.state = NightState(self.game)


class NightState(GameState):
    @property
    def can_act(self):
        return False

    def check_transition(self):
        if self.game.hour < BED_TIME:
            self.game.state = DayState(self.game)


async def idle():
    await asyncio.sleep(0)


class Game:
    def __init__(self):
        clear()
        print_title("🌾 WELCOME TO HAY DAY LITE 🌾")
        print("Survive as long as you can before running out of money.")
        print("Each day tax increases and market stock resets.")
        print_separator()

        while True:
            player_name = input("Enter your name: ").strip()
            if player_name:
                break
            print("Name cannot be empty. Please enter your name.")

        self.player = Player(player_name)
        self.market = Market()
        self.farm = Farm(self.player)
        self.facade = GameFacade(self.player, self.market, self.farm)

        self.day = 1
        self.hour = WAKE_UP_HOUR
        self.state = DayState(self)
        self.market.generate_stock()

        for i in range(3):
            obj = Wheat()
            self.farm.objects.append(obj)
            self.farm.current_used += obj.size

        print("\n--- Game Setup Complete ---")
        input("Press Enter to start farming...")

    def advance_time(self, hours):
        self.hour += hours
        # state transition check
        self.state.check_transition()

        if self.hour >= BED_TIME:
            print(f"\n💤 It's {self.hour:02d}:00! The farmer is tired and goes to sleep...")
            self.hour = 24
            self.end_day()
        elif self.hour >= 24:
            self.hour -= 24
            self.end_day()

    def end_game(self, reason="quit"):
        clear()
        print("\n" + "🌟" * (SEPARATOR_LENGTH // 2))

        if reason == "game_over":
            print("💀💀💀 GAME OVER! 💀💀💀".center(SEPARATOR_LENGTH))
            print("\n❌ BANKRUPT! You ran out of money and failed to pay the daily tax.")
            final_message = "Maybe next time you can harvest more!"
        else:
            print("👋👋👋 GAME ENDED 👋👋👋".center(SEPARATOR_LENGTH))
            print("\nYou decided to retire from farming.")
            final_message = "Thank you for playing!"

        print_separator()
        survival_day = self.day if reason == "quit" else self.day - 1

        print(f"🧑‍🌾 Farmer: {self.player.name.upper()}")
        print(f"⭐ Final Level: {self.player.level}")
        print(f"🗓️ Survived Until: Day {survival_day}")
        print(f"💰 Remaining Money: ${self.player.money}")

        print_separator()
        print(final_message)
        print("🌟" * (SEPARATOR_LENGTH // 2))
        sys.exit()

    def show_rules(self):
        clear()
        print_title("📜 GAME RULES 📜")
        print("\n1. OBJECTIVE")
        print_separator()
        print("  - Survive as long as possible by maintaining positive money.")
        print("  - Game over if money is < $0 after paying the daily tax.")

        print("\n2. TIME & DAILY CYCLE")
        print_separator()
        print(f"  - ⏰ Active Hours: {WAKE_UP_HOUR:02d}:00 to {BED_TIME:02d}:00.")
        print("  - Watering/Feeding costs 1 hour per successful action.")
        print("  - Reaching 22:00 or choosing 'Harvest & Collect' ends the day.")

        print("\n3. ECONOMY & GROWTH")
        print_separator()
        print("  - 💸 Daily Tax: Paid at day's end (increases daily).")
        print("  - Sell products at the Market to earn money.")
        print("  - 🌟 Level Up: Earn EXP from harvesting/collecting. Increases Farm/Inventory size.")
        print("  - ⚠️ Neglect: If not taken care of, growth reduces by 1. The object dies immediately if growth reaches -1.")

        print("\n" + "=" * SEPARATOR_LENGTH)
        input("Press Enter to return to the Main Menu...")

    def end_day(self):
        tax = 5 + (self.day - 1) * 2
        print("\n" + "=" * SEPARATOR_LENGTH)
        print(f"☀️ END OF DAY {self.day} ☀️".center(SEPARATOR_LENGTH))
        print_separator()

        # Neglect Check and Status Reset
        self.farm.reset_daily_statuses()

        # Tax Payment
        print(f"💸 Daily Tax Paid: -${tax}")
        self.player.change_money(-tax)

        # Game Over Check
        if self.player.money < 0:
            self.end_game(reason="game_over")

        print(f"💰 Remaining Money: ${self.player.money}")
        self.day += 1
        self.market.generate_stock()
        print_separator()
        self.hour = WAKE_UP_HOUR
        # ensure state
        self.state = DayState(self)
        print(f"🌅 WELCOME TO DAY {self.day}! ({self.hour:02d}:00) 🌅".center(SEPARATOR_LENGTH))
        print("=" * SEPARATOR_LENGTH)
        input("Press Enter to continue...")
        clear()

    def actions(self):
        while True:
            asyncio.run(idle())
            clear()
            self.facade.show_status(self.day, self.hour)
            self.farm.show_farm()
            self.player.inventory.show_inventory()

            print("\n" + "=" * SEPARATOR_LENGTH)
            print("📜 MAIN MENU:")
            print("=" * SEPARATOR_LENGTH)

            can_act = self.state.can_act

            def menu_item(num, text):
                return f" {num:<4} {text}"

            if not can_act:
                print(menu_item(" ", f"❌ Time is late ({BED_TIME:02d}:00)! Choose 3 to end day"))
                print(menu_item("1️⃣", "Water plants (N/A)"))
                print(menu_item("2️⃣", "Feed animals (N/A)"))
            else:
                print(menu_item("1️⃣", "Water plants (💧 +1 hour per plant)"))
                print(menu_item("2️⃣", "Feed animals (🥕 +1 hour per animal)"))

            print(menu_item("3️⃣", "Harvest & Collect (🌾🥚 END DAY/Collect All)"))
            print(menu_item("4️⃣", "Market Menu (🛒 Buy/Sell)"))
            print(menu_item("5️⃣", "View Game Rules (📚)"))
            print(menu_item("6️⃣", "Quit game (🚪)"))
            print("=" * SEPARATOR_LENGTH)

            choice = input("Choose action (1-6): ").strip().lower()

            if choice in ["1", "2", "4"] and not can_act:
                print("❌ You are too tired for this activity. Time to sleep!")

            elif choice == "1" and can_act:
                waterable_items = [
                    f"{i+1}. {o.name} ({o.growth}/{o.max_growth})"
                    for i, o in enumerate(self.farm.objects)
                    if isinstance(o, Plant)
                    and o.growth < o.max_growth
                    and not o._action_done_today
                ]

                if not waterable_items:
                    print("⚠️ No plants available to water (either fully grown, already watered, or none planted).")
                else:
                    print("\n💧 Available Plants to Water:")
                    for item in waterable_items:
                        print(f" - {item}")

                    indices_str = input("Enter plant numbers to water (e.g., 1,3): ").strip()
                    actions_done = self.facade.perform_actions(indices_str, 'water')
                    if actions_done > 0:
                        self.advance_time(actions_done)

            elif choice == "2" and can_act:
                feedable_items = []
                for i, o in enumerate(self.farm.objects):
                    if isinstance(o, Animal):
                        if o.growth < o.max_growth and not o._action_done_today:
                            feedable_items.append(f"{i+1}. {o.name} ({o.growth}/{o.max_growth})")

                if not feedable_items:
                    print("⚠️ No animals available to feed (either ready to produce, already fed, or none).")
                else:
                    print("\n🥕 Available Animals to Feed:")
                    for item in feedable_items:
                        print(f" - {item}")

                    indices_str = input("Enter animal numbers to feed (e.g., 2,4): ").strip()
                    actions_done = self.facade.perform_actions(indices_str, 'feed')
                    if actions_done > 0:
                        self.advance_time(actions_done)

            elif choice == "3":
                harvested, items, exp = self.facade.harvest_collect_all()
                if harvested:
                    self.player.add_exp(exp)
                    print(f"🎉 Harvest & Collect Complete! Total EXP gained: {exp}")
                else:
                    print("⚠️ Nothing was ready to harvest or collect, or inventory is full.")
                self.end_day()

            elif choice == "4" and can_act:
                self.market_menu()

            elif choice == "5":
                self.show_rules()

            elif choice == "6":
                self.end_game(reason="quit")

            else:
                print("❌ Invalid choice!")
            input("\nPress Enter to continue...")

    def market_menu(self):
        while True:
            clear()
            print_title("🏪 MARKET PLACE 🏪")
            print(f"💰 Your Current Money: ${self.player.money}")
            print("=" * SEPARATOR_LENGTH)

            self.facade.show_market()
            self.facade.show_inventory()

            print("\n" + "=" * SEPARATOR_LENGTH)
            print("MARKET OPTIONS:")
            print("=" * SEPARATOR_LENGTH)

            def market_item(num, text):
                return f" {num:<4} {text}"

            print(market_item("1️⃣", "Buy item (Seed/Animal)"))

            inventory_empty = self.player.inventory.is_empty()
            if inventory_empty:
                print(market_item("2️⃣", "Sell product (Inventory Empty 🎒)"))
            else:
                print(market_item("2️⃣", "Sell product (Harvest/Collection results)"))

            print(market_item("3️⃣", "Back to Main Menu"))
            print("=" * SEPARATOR_LENGTH)

            choice = input("Choose option (1-3): ").strip()

            if choice == "1":
                item = input("Enter item name to buy (e.g., Wheat, Cow): ").strip()
                try:
                    qty = int(input("Enter quantity to buy: "))
                    self.facade.buy_item(item, qty)
                except ValueError:
                    print("❌ Invalid quantity entered. Please enter a number.")
            elif choice == "2":
                if inventory_empty:
                    print("\n❌ Cannot sell: Your inventory is empty!")
                else:
                    item = input("Enter product name to sell (e.g., Wheat, Egg): ").strip()
                    try:
                        qty = int(input("Enter quantity to sell: "))
                        self.facade.sell_item(item, qty)
                    except ValueError:
                        print("❌ Invalid quantity entered. Please enter a number.")
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice!")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    game = Game()
    game.actions()