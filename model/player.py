from typing import List, Any

class Player:
    def __init__(self, name: str, class_name: str, hp: int, sp: int, attack: int, defense: int) -> None:
        self.name: str = name
        self.class_name: str = class_name
        self.hp: int = hp
        self.sp: int = sp
        self.attack: int = attack
        self.defense: int = defense
        self.inventory: List[Any] = []
        self.gold: int = 100

    def __str__(self) -> str:
        return f"""Player {self.name},
            Class name: {self.class_name},
            HP: {self.hp}, 
            SP: {self.sp}, 
            Attack: {self.attack}, 
            Defence: {self.defense},
            Gold: {self.gold}"""
    
    def get_name(self) -> str:
        return self.name

    def get_class_name(self) -> str:
        return self.class_name

    def get_hp(self) -> int:
        return self.hp

    def get_sp(self) -> int:
        return self.sp

    def get_attack(self) -> int:
        return self.attack

    def get_defense(self) -> int :
        return self.defense

    
    def update_stat(self, stat_name, value) -> None:
        if hasattr(self, stat_name):
            if stat_name == "hp":
                self.hp = max(self.hp - value, 0)
            else:
                setattr(self, stat_name, value)
        else:
            raise ValueError(f"Element '{stat_name}' not founded.")
        
    def add_item(self, item: Any) -> None:
        self.inventory.append(item)

    def remove_item(self, index: int)  -> None:
        if 0 <= index < len(self.inventory):
            del self.inventory[index]
        else:
            raise IndexError("Invalid inventory index")

    def get_inventory(self) -> List[Any]:
        return self.inventory
    
    def add_gold(self, amount: int) -> None:
        self.gold += amount

    def get_gold(self) -> int:
        return self.gold
        
    def remove_gold(self, amount: int) -> bool:
        if self.gold >= amount:
            self.gold -= amount
            return True
        else:
            return False

    