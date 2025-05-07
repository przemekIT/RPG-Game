class Player():
    def __init__(self, name, class_name, hp, sp, attack, defense):
        self.name = name
        self.class_name = class_name
        self.hp = hp
        self.sp = sp
        self.attack = attack
        self.defense = defense

    def __str__(self) -> str:
        return f"""Player {self.name},
            Class name: {self.class_name},
            HP: {self.hp}, 
            SP: {self.sp}, 
            Attack: {self.attack}, 
            Defence: {self.defense}"""
    
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

    