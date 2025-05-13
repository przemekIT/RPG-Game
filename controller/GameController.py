import tkinter as tk
from view.GameGUI import GameGUI
from view.CreateGame import CreateGame
from view.GameScreen import GameScreen
from view.LoadGame import LoadGame
from model.GameCharacter import GameCharacter
import json
from pathlib import Path
import random
import threading
import time
from typing import Any, Optional, Union, List, Tuple, Dict, Callable

class GameController:
    ESCAPE_CHANCE: float = 0.3
    ENEMY_HIT_CHANCE: float = 0.5
    DROP_CHANCE: float = 0.4

    def __init__(self):
        self.root: tk.Tk = tk.Tk()
        self.save_data: str = "assets/save.json"
        
        self.data_player: dict = self.load_data("assets/characters.json")
        self.dataGUI: dict = self.load_data("assets/mainGUI.json")
        self.data_items: dict = self.load_data("assets/items.json")
        self.load_save: dict = self.load_data(self.save_data)
        
        self.load_list: List[Tuple[str, Optional[dict]]] = []
        self.create_load_list()

        self.gui: GameGUI = GameGUI(self.root, self.dataGUI, self)
        self.characters: GameCharacter = GameCharacter(self.data_player, self.data_items)

        self.current_zon: Optional[str] = None
        self.zone_steps: int = 0
        self.inventory_items: List[Any] = []
        self.inventory_buttons: List[Any] = []
        self.curently_frame: Optional[Any] = None
        self.curently_buttons: Optional[Any] = None

        self.player: Optional[Any] = None
        self.enemys: List[Any] = []
        self.npcs: List[Any] = []
        self.starter_items: List[Any] = []

        self.new_create: Optional[CreateGame] = None
        self.load_game_screen: Optional[LoadGame] = None

        self.game_screen: Optional[GameScreen] = None
        self.starting_enemy_hp: Optional[int] = None
        self.stop_waiting: bool = False
        self.can_save_game: bool = False
        self.can_return: bool = False

    def load_data(self, file: str) -> dict:
        basePath = Path(__file__).parent
        file_path = (basePath / ".." / file ).resolve()
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: {file} not found!")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode {file}")
            return {}

    def saveing(self, slot: str) -> None:
        cz = self.current_zon
        if isinstance(cz, str):
            current_zone_str = cz
        elif cz is None:
            current_zone_str = ""
        else:
            current_zone_str = ""
        save_data = {
            "name": self.player.get_name(),
            "class_name": self.player.get_class_name(),
            "hp": self.player.get_hp(),
            "sp": self.player.get_sp(),
            "attack": self.player.get_attack(),
            "defence": self.player.get_defense(),
            "gold": self.player.get_gold(),
            "inventory": [item.to_dict() for item in self.player.get_inventory()],
            "current_zone": current_zone_str,
            "zone_steps": self.zone_steps
        }

        basePath = Path(__file__).parent
        file_path = (basePath / ".." / self.save_data).resolve()

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                saves = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            saves = {"save1": None, "save2": None, "save3": None}

        if slot == "save1":
            saves["save1"] = save_data
        elif slot == "save2":
            saves["save2"] = save_data
        elif slot == "save3":
            saves["save3"] = save_data

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(saves, f, indent=4, ensure_ascii=False)

        self.game_screen.update_event_log(f"Game successfully saved in {slot}")
        self.wait_and_continue()

    def save_game(self) -> None:
        self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
        self.game_screen.create_save_game_buttons(self.load_list)
        

    def load_game(self) -> None:
        self.gui.clear_screen()
        self.load_game_screen = LoadGame(
            parent=self.gui.main_frame,
            saves_list=self.load_list,
            select_callback=self.load_selected_game,
            back_callback=self.gui.create_main_menu
        )

    def load_selected_game(self, slot: str) -> None:
        save_entry = self.load_save.get(slot)

        if not save_entry:
            return
        
        self.player = self.characters.load_player(save_entry)
        self.current_zon = save_entry.get("current_zone", "")
        self.zone_steps = save_entry.get("zone_steps", 0)
        self.create_after_load_game()
        self.start_game()
            
    def create_load_list(self) -> None:
        for slot in ['save1', 'save2', 'save3']:
            save_data = self.load_save.get(slot)

            if save_data and "name" in save_data and "class_name" in save_data:
                self.load_list.append((slot, save_data)) 
            else:
                self.load_list.append((slot, None)) 
        

    def new_game(self) -> None:
        self.gui.clear_screen()
        self.new_create = CreateGame(self.gui.main_frame, self)

    def create_after_load_game(self) -> None:
        self.enemys = self.characters.create_enemy()
        self.npcs = self.characters.create_nps()
        self.starter_items = self.characters.set_objects()

    def create_character(self, name: str, char_class: str) -> None:
        self.player = self.characters.create_player(name, char_class)
        self.create_after_load_game()

        sword = next((item for item in self.starter_items if item.get_item() == "Sword"), None)
        if sword:
            self.player.add_item(sword.clone())
        
        self.start_game()

    def start_game(self) -> None:
        self.gui.clear_screen()
        self.game_screen = GameScreen(self.root, self, self.dataGUI)
        self.update_player_info()

        self.update_inventory_bar(self.player.get_inventory())

        self.curently_buttons = self.game_screen.create_start_action_buttons
        

    def update_player_info(self) -> None:
        self.game_screen.clear_frame(self.game_screen.right_frame)
        self.game_screen.player_info(self.player)

    def update_enemy_info(self) -> None:
        self.game_screen.clear_frame(self.game_screen.left_frame)
        self.game_screen.enemy_info(self.enemy)

    def generate_loot(self)-> Optional[Any]:
        if random.random() > GameController.DROP_CHANCE:
            return None

        all_items = self.characters.get_object()
        loot_template = random.choice(all_items)

        loot = loot_template.clone()

        if loot.get_type() == "weapon" and "attack" in loot.get_stat():
            base_attack = loot.get_stat()["attack"]
            new_attack = base_attack + random.randint(-10, 10)
            loot.set_stat({"attack": max(new_attack, 1)})
        elif loot.get_type() == "armor" and "defense" in loot.get_stat():
            base_defense = loot.get_stat()["defense"]
            new_defense = base_defense + random.randint(-5, 5)
            loot.set_stat({"defense": max(new_defense, 1)})

        self.game_screen.clear_frame(self.game_screen.left_frame)
        self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
        self.game_screen.show_item_info(loot)

        def add_to_inventory():
            inventory = self.player.get_inventory()
            if len(inventory) >= 10:
                self.game_screen.update_event_log("Inventar is full")
                self.wait_and_continue()
            else:
                inventory.append(loot)
                self.update_inventory_bar(inventory)
                self.game_screen.update_event_log(f"You add {loot.get_item()} to inventar")
                self.wait_and_continue()
        def discard_loot():
            self.game_screen.update_event_log(f"You discarded {loot.get_item()}.")
            self.wait_and_continue()

        self.game_screen._create_hover_button(self.game_screen.center_buttons_frame, "Add to Inventory",
                                        add_to_inventory, bg="#ccffcc", hover_bg="#99ff99")
        self.game_screen._create_hover_button(self.game_screen.center_buttons_frame, "Discard Item",
                                        discard_loot, bg="#ffcccc", hover_bg="#ff9999")
        
        return loot

    def drop_item(self, index: int) -> None:
        del self.player.inventory[index]
        self.update_inventory_bar(self.player.inventory)
        self.game_screen.update_event_log(f"Drop Item")
        # self.game_screen.clear_frame(self.game_screen.center_buttons_frame)

    def go_to_castle(self)-> None:
        self.zone_steps = 0
        self.current_zon = self.go_to_castle

        self.wait_and_continue()

    def go_to_forest(self)-> None:
        # self.zone_steps = 0
        self.game_screen.update_event_log("The location you're trying to visit is not yet ready.")

    def go_to_gate(self)-> None:
        # self.zone_steps = 0
        self.game_screen.update_event_log("The location you're trying to visit is not yet ready.")

    def random_event(self) -> str:
        events = ["battle", "peaceful"]
        return random.choice(events)

    def return_to_main_actions(self)-> None:
        self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
        self.game_screen.clear_frame(self.game_screen.left_frame)
        self.game_screen.create_start_action_buttons()
        self.game_screen.update_event_log("--- Returned to main actions ---")

    def attack_action(self)-> None:
        player_attack = self.player.get_attack()
        enemy_defense = self.enemy.get_defense()

        self.starting_enemy_hp = self.enemy.get_hp()

        damage_to_enemy = max(player_attack - enemy_defense, 0)
        self.enemy.update_stat("hp", damage_to_enemy)

        self.update_enemy_info()
        self.game_screen.update_event_log(f"{self.enemy.name} - {damage_to_enemy} damage")

        if self.enemy.hp <= 0:
            self.game_screen.update_event_log(f"{self.enemy.name} - is Die")

            gained_sp = int(self.starting_enemy_hp / 10)
            current_sp = self.player.get_sp()
            self.player.update_stat("sp", current_sp + gained_sp)

            loot = self.generate_loot()
            if loot is None:
                return self.go_to_castle()
            else:
                return

        if random.random() < GameController.ENEMY_HIT_CHANCE:
            damage_to_player = max(self.enemy.get_attack() - self.player.get_defense(), 0)
            self.player.update_stat("hp", damage_to_player)

            self.update_player_info()
            self.game_screen.update_event_log(f"{self.player.name} - {damage_to_player} damage")

            if self.player.hp <= 0:
                self.game_screen.update_event_log("You die!")
        self.zone_steps += 1

    def defend_action(self)-> None:
        if random.random() < GameController.ENEMY_HIT_CHANCE:
            damage_to_player = max(self.enemy.get_attack() - self.player.get_defense(), 0)
            self.player.update_stat("hp", damage_to_player)
            self.game_screen.update_event_log(f"You defend! {self.enemy.name} deals {damage_to_player} damage")

        else:
            self.game_screen.update_event_log(f"{self.enemy.name} missed the attack!")

        self.update_player_info()

        if self.player.hp <= 0:
            self.game_screen.update_event_log("You die!")

        self.zone_steps += 1

    def run_action(self) -> Optional[Callable[[], None]]:
        if random.random() < GameController.ESCAPE_CHANCE:
            self.game_screen.update_event_log(f"{self.player.name} successfully fled from the battle!")
            return self.current_zon()

        self.game_screen.update_event_log(f"{self.player.name} failed to escape!")

        if random.random() < GameController.ENEMY_HIT_CHANCE:
            damage_to_player = max(self.enemy.get_attack() - self.player.get_defense(), 0)
            self.player.update_stat("hp", damage_to_player)
            self.update_player_info()
            self.game_screen.update_event_log(f"{self.player.name} receives {damage_to_player} damage!")

            if self.player.hp <= 0:
                self.game_screen.update_event_log("You die!")

        self.zone_steps += 1

    def wait_and_continue(self) -> None:
        self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
        self.game_screen.clear_frame(self.game_screen.left_frame)

        self.stop_waiting = False
        self.can_save_game = True

        def return_home():
            self.stop_waiting = True
            self.return_to_main_actions() 

        def save_game():
            self.stop_waiting = True
            self.save_game()

        self.can_return = self.zone_steps >= 15


        self.game_screen.create_return_home_and_save_buttons(
            return_command=return_home,
            save_command=save_game,
            return_enabled=self.can_return,
            save_enabled=self.can_save_game
        ) 

        def delayed_event():
            time.sleep(3)
            if not self.stop_waiting:
                self.root.after(0, self.zone_event)

        threading.Thread(target=delayed_event, daemon=True).start()

    def zone_event(self) -> None:
        event = self.random_event()
        self.game_screen.clear_frame(self.game_screen.left_frame)
        self.game_screen.clear_frame(self.game_screen.center_buttons_frame)

        if event == "battle":
            self.enemy = self.characters.get_random_enemy()
            self.update_enemy_info()
            self.game_screen.create_battle_action_buttons()

            self.curently_frame = self.update_enemy_info
            self.curently_buttons = self.game_screen.create_battle_action_buttons

        elif event == "peaceful":
            self.npc = self.characters.get_random_nps()
            self.game_screen.npc_info(self.npc)
            self.game_screen.create_npc_action_buttons(self.npc)

            self.curently_frame = self.game_screen.npc_info
            self.curently_buttons = self.game_screen.create_npc_action_buttons
        
        self.zone_steps += 1

    def npc_action(self, npc, service: str) -> None:
        def back_to_npc_menu():
            self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
            self.game_screen.create_npc_action_buttons(npc)

        def refresh_inventory_bar():
            self.game_screen.update_inventory_bar(self.player.get_inventory())

        self.game_screen.clear_frame(self.game_screen.center_buttons_frame)

        inventory = self.player.get_inventory()
        gold = getattr(self.player, 'gold', 0)

        if service == "Sell Items":
            self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
            self.game_screen.update_event_log(f"Choose item to sell to {npc.name}...")

            inventory = self.player.get_inventory()
            if not inventory:
                self.game_screen.update_event_log("Your inventory is empty. Nothing to sell.")
                self.game_screen._create_hover_button(
                    self.game_screen.center_buttons_frame,
                    "Back",
                    lambda: self.game_screen.create_npc_action_buttons(npc),
                    bg="#ffcccc", hover_bg="#ff9999"
                )
                return

            for index, item in enumerate(inventory):
                item_name = item.get_item()
                self.game_screen._create_hover_button(
                    self.game_screen.center_buttons_frame,
                    f"Sell {item_name}",
                    command=lambda i=item, idx=index, n=npc: self.sell_item_and_refresh(i, idx, n),
                    bg="#d9d9d9", hover_bg="#c0c0c0"
                )

            self.game_screen._create_hover_button(
                self.game_screen.center_buttons_frame,
                "Back",
                lambda: self.game_screen.create_npc_action_buttons(npc),
                bg="#ffcccc", hover_bg="#ff9999"
            )
        elif service in ["Upgrade Weapons", "Upgrade Armor"]:
            upgrade_type = "weapon" if service == "Upgrade Weapons" else "armor"
            stat_key = "attack"
            self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
            self.game_screen.update_event_log(f"Choose {upgrade_type} to upgrade...")

            inventory = self.player.get_inventory()

            def back_to_npc_menu():
                self.game_screen.create_npc_action_buttons(npc)

            def refresh_inventory_bar():
                self.update_inventory_bar(inventory)
                self.update_player_info()

            items = [item for item in inventory if item.get_type() == upgrade_type and stat_key in item.get_stat()]

            if not items:
                self.game_screen.update_event_log(f"You have no {upgrade_type} to upgrade.")
                self.game_screen._create_hover_button(
                    self.game_screen.center_buttons_frame, "Back",
                    back_to_npc_menu, bg="#ffcccc", hover_bg="#ff9999"
                )
                return

            for item in items:
                item_name = item.get_item()
                current_stat = item.get_stat().get(stat_key, 0)
                upgrade_cost = current_stat

                def make_upgrade_command(i=item, key=stat_key, cost=upgrade_cost):
                    def upgrade():
                        if self.player.gold >= cost:
                            self.player.gold -= cost
                            new_value = i.get_stat()[key] + 1
                            i.set_stat({key: new_value})
                            refresh_inventory_bar()
                            self.game_screen.update_event_log(f"You upgraded {i.get_item()} (+1 {key}) for {cost} gold.")
                            self.game_screen.update_player_info()

                            self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
                            self.game_screen._create_hover_button(
                                self.game_screen.center_buttons_frame, "Back",
                                back_to_npc_menu, bg="#ffcccc", hover_bg="#ff9999"
                            )
                        else:
                            self.game_screen.update_event_log("Not enough gold to upgrade!")
                    return upgrade

                self.game_screen._create_hover_button(
                    self.game_screen.center_buttons_frame,
                    f"Upgrade {item_name} - Cost: {upgrade_cost} gold",
                    make_upgrade_command(),
                    bg="#ccffcc", hover_bg="#99ff99"
                )

            self.game_screen._create_hover_button(
                self.game_screen.center_buttons_frame, "Back",
                back_to_npc_menu, bg="#ffcccc", hover_bg="#ff9999"
            )

        elif service == "Heal":
            self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
            self.game_screen.update_event_log(f"{npc.name} offers to heal you...")

            def back_to_npc_menu():
                self.game_screen.create_npc_action_buttons(npc)

            player_hp = self.player.hp
            max_hp = 100
            missing_hp = max_hp - player_hp

            if missing_hp == 0:
                self.game_screen.update_event_log("You are already at full HP!")
                self.game_screen._create_hover_button(
                    self.game_screen.center_buttons_frame, "Back",
                    back_to_npc_menu, bg="#ffcccc", hover_bg="#ff9999"
                )
                return

            heal_cost = missing_hp

            def heal_action():
                gold_available = self.player.gold
                heal_amount = min(missing_hp, gold_available)

                if heal_amount > 0:
                    self.player.gold -= heal_amount
                    self.player.update_stat("hp", -heal_amount)
                    self.update_player_info()
                    self.game_screen.update_event_log(f"{npc.name} healed you for {heal_amount} HP for {heal_amount} gold.")
                else:
                    self.game_screen.update_event_log("Not enough gold to heal!")

                self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
                self.game_screen._create_hover_button(
                    self.game_screen.center_buttons_frame, "Back",
                    back_to_npc_menu, bg="#ffcccc", hover_bg="#ff9999"
                )

            self.game_screen._create_hover_button(
                self.game_screen.center_buttons_frame,
                f"Heal ({missing_hp} HP) - Cost: {heal_cost} gold",
                heal_action,
                bg="#ccffcc", hover_bg="#99ff99"
            )

            self.game_screen._create_hover_button(
                self.game_screen.center_buttons_frame, "Back",
                back_to_npc_menu, bg="#ffcccc", hover_bg="#ff9999"
            )

        elif service == "Buy Potions":
            potion = self.create_potion()
            if potion:
                inventory = self.player.get_inventory()
                if len(inventory) >= 10:
                    self.game_screen.update_event_log("Your inventory is full. Cannot buy potion.")
                else:
                    inventory.append(potion)
                    self.player.gold -= potion.get_stat_text()
                    self.game_screen.update_inventory_bar(inventory)
                    self.update_player_info()
                    self.game_screen.update_event_log(f"You bought a Health Potion from {npc.name} for 10 gold.")
            else:
                self.game_screen.update_event_log("No potion template found!")

        elif service == "Buy Items":
            inventory = self.player.get_inventory()
            all_items = self.characters.get_object()
            loot_template = random.choice(all_items)
            item = loot_template.clone()

            # Price = 2 * sum(stats)
            price = 2 * sum(item.get_stat().values())

            def refresh_inventory_bar():
                self.game_screen.update_inventory_bar(inventory)
                self.update_player_info()

            def back_to_npc_menu():
                self.game_screen.create_npc_action_buttons(npc)

            def buy_item():
                if self.player.gold >= price:
                    if len(inventory) >= 10:
                        self.game_screen.update_event_log("Inventory is full! Cannot buy item.")
                        return
                    self.player.gold -= price
                    inventory.append(item)
                    refresh_inventory_bar()
                    self.game_screen.update_event_log(f"You bought {item.get_item()} for {price} gold.")

                    self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
                    self.game_screen._create_hover_button(
                        self.game_screen.center_buttons_frame, "Back",
                        back_to_npc_menu, bg="#ffcccc", hover_bg="#ff9999"
                    )
                else:
                    self.game_screen.update_event_log("Not enough gold to buy item!")

            self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
            self.game_screen.clear_frame(self.game_screen.left_frame)
            self.game_screen.show_item_info(item)

            self.game_screen._create_hover_button(
                self.game_screen.center_buttons_frame,
                f"Buy {item.get_item()} ({price} gold)",
                buy_item,
                bg="#ccffcc", hover_bg="#99ff99"
            )

            self.game_screen._create_hover_button(
                self.game_screen.center_buttons_frame, "Back",
                back_to_npc_menu, bg="#ffcccc", hover_bg="#ff9999"
            )

        elif service in ["Give Information", "Offer Side Quest"]:
            self.game_screen.update_event_log(f"{service} is under development...")
            self.zone_event()

        else:
            self.game_screen.update_event_log("Unknown service")
            print("Unknown service")
        
    def create_potion(self):
        all_items = self.characters.get_object()
        for item in all_items:
            if item.get_item() == "Health Potion":
                return item.clone()
        return None

    def sell_item_and_refresh(self, item, index: int, npc) -> None:
        self.sell_item(item, index, npc)
        self.game_screen.update_inventory_bar(self.player.get_inventory())
        self.npc_action(npc, "Sell Items")

    def use_item(self, item) -> None:
        item_type = item.get_type()
        item_stats = item.get_stat()
        if item_type == "weapon":
            attack_bonus = item_stats.get("attack", 0)
            if attack_bonus > 0:
                self.player.update_stat("attack", self.player.get_attack() + attack_bonus)
                self.game_screen.update_event_log(f"Used weapon: {item.get_item()} - Attack increased by {attack_bonus}")
                self.game_screen.clear_frame(self.game_screen.right_frame)
                self.game_screen.update_player_info()
        
        elif item_type == "armor":
            defense_bonus = item_stats.get("defense", 0)
            if defense_bonus > 0:
                self.player.update_stat("defense", self.player.get_defense() + defense_bonus)
                self.game_screen.update_event_log(f"Used armor: {item.get_item()} - Defense increased by {defense_bonus}")
                self.game_screen.clear_frame(self.game_screen.right_frame)
                self.game_screen.update_player_info()
        
        else:
            self.game_screen.update_event_log(f"Item {item.get_item()} cannot be used.")
        

    def sell_item(self, item, index: int, npc) -> None:
        npc_role = npc.role.lower()
        item_type = item.get_type()
        item_stats = item.get_stat()

        if item_type == "weapon" and "attack" in item_stats:
            stat_value = item_stats["attack"]
            preferred_role = "blacksmith"
        elif item_type == "armor" and "defense" in item_stats:
            stat_value = item_stats["defense"]
            preferred_role = "blacksmith"
        elif item_type == "potion" and "heal" in item_stats:
            stat_value = item_stats["heal"]
            preferred_role = "healer"
        else:
            self.game_screen.update_event_log(f"Cannot sell {item.get_item()} — item type not recognized.")
            return

        if npc_role == preferred_role:
            price = stat_value
        else:
            price = max(stat_value // 2, 1)

        self.player.add_gold(price)
        self.player.remove_item(index)

        self.game_screen.update_inventory_bar(self.player.get_inventory())
        self.update_player_info()

        self.game_screen.update_event_log(f"Sold {item.get_item()} for {price} gold to {npc.name} ({npc_role}).")

    def update_inventory_bar(self, items) -> None:
        self.inventory_items = items

        for i in range(10):
            if i < len(items):
                item = items[i]
                self.inventory_buttons[i].config(text=item.get_item())
            else:
                self.inventory_buttons[i].config(text="Empty")

    def create_inventory_bar(self, btn: 'tk.Button') -> None:
        self.inventory_buttons.append(btn)

    def on_inventory_click(self, index: int) -> None:
        self.game_screen.clear_frame(self.game_screen.left_frame)
        self.game_screen.clear_frame(self.game_screen.center_buttons_frame)

        if index < len(self.inventory_items):
            item = self.inventory_items[index]
            self.game_screen.show_item_info(item)
            self.game_screen.show_inventory_actions(item, index)
        else:
            pass

    def inventory_actions(self, item, index: int) -> None:
        self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
        self.game_screen.show_inventory_actions(item, index)

    def go_back(self) -> None:   
        self.game_screen.clear_frame(self.game_screen.left_frame)
        self.game_screen.clear_frame(self.game_screen.center_buttons_frame) 
        if self.curently_frame:
            self.curently_frame()    
        if self.curently_buttons:
            self.curently_buttons()     

    def run(self) -> None:
        self.root.mainloop()