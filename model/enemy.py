class Enemy():
    def __init__(self, name, hp, attack, defense, exp, description):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.description = description

    def __str__(self) -> str:
        return f"""
            Enemy {self.name}
            Description: {self.description}
            HP: {self.hp}
            Attack: {self.attack}
            Defense: {self.defense}
            EXP Reward: {self.exp}
            """
    
    def clone(self) -> 'Enemy':
        return Enemy(self.name, self.hp, self.attack, self.defense, self.exp, self.description)
    
    def get_name(self) -> str:
        return self.name

    def get_hp(self) -> int:
        return self.hp

    def get_attack(self) -> int:
        return self.attack

    def get_defense(self) -> int:
        return self.defense

    def get_exp(self) -> int:
        return self.exp

    def get_description(self) -> str:
        return self.description
    
    def update_stat(self, stat_name, value) -> None:
        if hasattr(self, stat_name):
            if stat_name == "hp":
                self.hp = max(self.hp - value, 0)
            else:
                setattr(self, stat_name, value)
        else:
            raise ValueError(f"Element '{stat_name}' not founded.")
