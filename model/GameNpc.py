import random
from typing import List

class GameNpc:
    def __init__(self, name: str, role: str, description: str, services: List[str], location: str, dialogue: List[str]) -> None:
        self.name: str = name
        self.role: str = role
        self.description: str = description
        self.services: List[str] = services
        self.location: str = location
        self.dialogue: List[str] = dialogue

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
    def get_role(self) -> str:
        return self.role
    
    def clone(self) -> 'GameNpc':
        return GameNpc(self.name, self.role, self.description, self.services, self.location, self.get_random_dialogue())

