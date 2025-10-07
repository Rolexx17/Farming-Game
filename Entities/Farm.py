from Entities.Farm_Object import Plant, Animal
from Entities.Utils import SEPARATOR_LENGTH, print_separator

class Farm:
    def __init__(self, player):
        self.player = player
        self.objects = []
        self.current_used = 0

    def add_object(self, obj):
        if self.current_used + obj.size > self.player.farm_size:
            return False
        self.objects.append(obj)
        self.current_used += obj.size
        return True

    def show_farm(self):
        print("\n" + "=" * SEPARATOR_LENGTH)
        print("🚜 FARM STATUS")
        print_separator()
        
        if not self.objects:
            print(" - No plants or animals on your farm yet.")
        else:
            for i, o in enumerate(self.objects):
                status_text = "READY!" if o.harvestable_or_collectable() else "Growing..."
                icon = "🌱" if isinstance(o, Plant) else "🐄"
                
                # Check for death/dying status based on growth
                if o.growth <= 0 and not o.harvestable_or_collectable():
                    status_text = "DYING!"
                    icon = "🥀" if isinstance(o, Plant) else "💀"
                elif o.growth == 1 and not o.harvestable_or_collectable():
                    status_text = "LOW GROWTH!"
                
                # Action status indicator
                action_status = "✅" if o._action_done_today else "❌"

                print(
                    f"[{i+1:<2}] {icon} {o.name:<11} ({o.size} slot) [{o.growth}/{o.max_growth:<2}] -> {status_text} (Action: {action_status})"
                )
                
        remaining = self.player.farm_size - self.current_used
        print_separator()
        print(f"SLOTS USED: {self.current_used}/{self.player.farm_size} | REMAINING SLOTS: {remaining}")

    def perform_action_on_selected(self, indices_str, action_type):
        successful_actions = 0
        try:
            temp = []
            for i in indices_str.split(','):
                clean_i = i.strip()
                if clean_i:
                    temp.append(int(clean_i))
            index = []
            for i in temp:
                index.append(i - 1)

        except ValueError:
            print("❌ Invalid input format. Please use numbers separated by commas (e.g., 1,3).")
            return 0

        valid_type = Plant if action_type == 'water' else Animal
        
        for i in index:
            if 0 <= i < len(self.objects):
                obj = self.objects[i]
                if isinstance(obj, valid_type):
                    if obj.action():
                        successful_actions += 1
                else:
                    print(f"⚠️ Item {i+1} ({obj.name}) is not a {action_type}able item.")
            else:
                print(f"⚠️ Item {i+1} is out of range.")
                
        if successful_actions > 0:
            print(f"✅ Action completed on {successful_actions} item(s). Time elapsed: {successful_actions} hour(s).")
            
        return successful_actions


    def harvest_collect_all(self):
        harvested_items = {}
        total_exp = 0
        
        objects_to_keep = []
        objects_to_reset = []
        
        print("\n--- Collecting Items ---")
        for o in self.objects:
            if o.harvestable_or_collectable():
                if self.player.inventory.add_item(o.product_name, 1):
                    harvested_items[o.product_name] = harvested_items.get(o.product_name, 0) + 1
                    total_exp += o.product_exp
                    print(f"✅ Gathered 1x {o.product_name} from {o.name}. (+{o.product_exp} EXP)")
                    
                    if isinstance(o, Plant):
                        self.current_used -= o.size
                        # Plant is implicitly removed
                    elif isinstance(o, Animal):
                        objects_to_reset.append(o)
                        objects_to_keep.append(o)
                else:
                    print(f"⚠️ Inventory full! Could not collect from {o.name}. Try selling items first.")
                    objects_to_keep.append(o)
            else:
                objects_to_keep.append(o)
                
        for o in objects_to_reset:
            o.reset_after_collection()
            
        self.objects = objects_to_keep
        
        harvested_count = sum(harvested_items.values())
        return harvested_count > 0, harvested_items, total_exp

    def reset_daily_statuses(self):
        # Check for Neglect
        print("\n--- Daily Maintenance Check ---")
        objects_after_neglect = []
        neglect_used_slots = 0

        for o in self.objects:
            if isinstance(o, Plant) or isinstance(o, Animal): 
                is_dead = o.check_daily_neglect()
                
                if not is_dead:
                    objects_after_neglect.append(o)
                    neglect_used_slots += o.size
                else:
                    # Item died, free up space
                    self.current_used -= o.size 
            else:
                 objects_after_neglect.append(o)
                 neglect_used_slots += o.size
        
        self.objects = objects_after_neglect
        self.current_used = neglect_used_slots
        
        # Reset Action Status
        for o in self.objects:
            if isinstance(o, Plant) or isinstance(o, Animal):
                o.reset_daily_status()
                
        print("--- Daily Maintenance Complete ---")