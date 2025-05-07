import random

class GameNpc:
    def __init__(self, name, role, description, services, location, dialogue):
        self.name = name
        self.role = role
        self.description = description
        self.services = services
        self.location = location
        self.dialogue = dialogue

    def get_random_dialogue(self) -> str:
        return random.choice(self.dialogue)
    
    def __str__(self) -> str:
        return f"""
            NPC: {self.name}
            Role: {self.role}
            Location: {self.location}
            Description: {self.description}
            Services: {", ".join(self.services)},
            Dialogue: {self.get_random_dialogue()}
            """
    
    def clone(self) -> 'GameNpc':
        return GameNpc(self.name, self.role, self.description, self.services, self.location, self.get_random_dialogue())

