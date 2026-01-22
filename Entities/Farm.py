from Entities.Farm_Object import Plant, Animal
from Entities.Utils import SEPARATOR_LENGTH, print_separator

class Farm:
    def __init__(self, player):
        self.player = player
        self.objects = [] # Composite of FarmObjects
        self.current_used = 0

    def add_object(self, obj):
        if self.current_used + obj.size > self.player.farm_size:
            return False
        self.objects.append(obj)
        self.current_used += obj.size
        return True

    def show_farm(self):
        print("\n" + "=" * SEPARATOR_LENGTH + "\n🚜 FARM STATUS")
        print_separator()
        if not self.objects:
            print(" - No plants or animals yet.")
        else:
            for i, o in enumerate(self.objects):
                status = "READY!" if o.harvestable_or_collectable() else "Growing..."
                icon = "🌱" if isinstance(o, Plant) else "🐄"
                act = "✅" if o._action_done_today else "❌"
                print(f"[{i+1:<2}] {icon} {o.name:<11} ({o.size} slot) [{o.growth}/{o.max_growth}] -> {status} ({act})")
        print_separator()
        print(f"SLOTS USED: {self.current_used}/{self.player.farm_size}")

    def perform_action_on_selected(self, indices_str, action_type):
        valid_indices = []
        try:
            valid_indices = [int(i.strip()) - 1 for i in indices_str.split(',') if i.strip()]
        except ValueError: return 0

        success = 0
        target_type = Plant if action_type == 'water' else Animal
        for i in valid_indices:
            if 0 <= i < len(self.objects):
                obj = self.objects[i]
                if isinstance(obj, target_type) and obj.action():
                    success += 1
        return success

    def harvest_collect_all(self, player):
        items_gained, total_exp = {}, 0
        keep, reset = [], []

        for o in self.objects:
            if o.harvestable_or_collectable():
                if player.inventory.add_item(o.product_name, 1):
                    items_gained[o.product_name] = items_gained.get(o.product_name, 0) + 1
                    total_exp += o.product_exp
                    if isinstance(o, Plant): self.current_used -= o.size
                    else: 
                        reset.append(o)
                        keep.append(o)
                else: keep.append(o)
            else: keep.append(o)

        for o in reset: o.reset_after_collection()
        self.objects = keep
        return len(items_gained) > 0, items_gained, total_exp

    def reset_daily_statuses(self):
        alive = []
        for o in self.objects:
            if o.check_daily_neglect():
                self.current_used -= o.size
                print(f"💀 Death: {o.name} died from neglect!")
            else:
                o.reset_daily_status()
                alive.append(o)
        self.objects = alive