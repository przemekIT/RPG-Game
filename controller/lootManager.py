class LootManager:
    DROP_CHANCE = 0.4

    def __init__(self, characters, player, game_screen):
        self.characters = characters
        self.player = player
        self.game_screen = game_screen

    def generate_loot(self):
        if random.random() > LootManager.DROP_CHANCE:
            return None

        all_items = self.characters.get_object()
        loot_template = random.choice(all_items)

        loot = loot_template.clone()

        # Modify loot properties
        if loot.get_type() == "weapon" and "attack" in loot.get_stat():
            base_attack = loot.get_stat()["attack"]
            new_attack = base_attack + random.randint(-10, 10)
            loot.set_stat({"attack": max(new_attack, 1)})
        elif loot.get_type() == "armor" and "defense" in loot.get_stat():
            base_defense = loot.get_stat()["defense"]
            new_defense = base_defense + random.randint(-5, 5)
            loot.set_stat({"defense": max(new_defense, 1)})

        self.game_screen.show_item_info(loot)

        def add_to_inventory():
            inventory = self.player.get_inventory()
            if len(inventory) >= 10:
                self.game_screen.update_event_log("Inventar is full")
            else:
                inventory.append(loot)
                self.game_screen.update_inventory_bar(inventory)
                self.game_screen.update_event_log(f"You add {loot.get_item()} to inventar")

        def discard_loot():
            self.game_screen.update_event_log(f"You discarded {loot.get_item()}.")

        self.game_screen._create_hover_button(self.game_screen.center_buttons_frame, "Add to Inventory",
                                              add_to_inventory, bg="#ccffcc", hover_bg="#99ff99")
        self.game_screen._create_hover_button(self.game_screen.center_buttons_frame, "Discard Item",
                                              discard_loot, bg="#ffcccc", hover_bg="#ff9999")
