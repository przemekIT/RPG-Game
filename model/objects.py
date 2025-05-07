class GameObjects:
    def __init__(self, data_items):
        self.weapons = data_items.get('weapons', [])
        self.armors = data_items.get('armors', [])
        self.consumables = data_items.get('consumables', [])

        self.player_inventory = []

    def get_all_items(self):
        return self.weapons + self.armors + self.consumables

    def add_to_inventory(self, item):
        if len(self.player_inventory) >= 10:
            print("Inventory is full!")
            return False
        self.player_inventory.append(item)
        return True

    def remove_from_inventory(self, item):
        if item in self.player_inventory:
            self.player_inventory.remove(item)
            return True
        print("Item not in inventory!")
        return False

    def clear_inventory(self):
        self.player_inventory.clear()

    def has_item(self, item_name):
        return any(item['name'] == item_name for item in self.player_inventory)

    def get_inventory(self):
        return self.player_inventory.copy()