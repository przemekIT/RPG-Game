class Enemy():
    def __init__(self, name, hp, attack, defense, exp, description):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.description = description

    def __str__(self):
        return f"""
            Enemy {self.name}
            Description: {self.description}
            HP: {self.hp}
            Attack: {self.attack}
            Defense: {self.defense}
            EXP Reward: {self.exp}
            """