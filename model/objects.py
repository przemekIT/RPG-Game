from typing import Dict, Any
class GameObjects:
    def __init__(self, name: str, type_: str, description: str, stat: int) -> None:
        self.name: str = name
        self.type: str = type_
        self.description: str = description
        self.stat: int = stat
        self.using: bool = False

    def __str__(self) -> str:
        return f"""
            Item: {self.name}
            Type: {self.type}
            Description: {self.description}
            Stat: {self.stat}
        """
    
    def get_item(self) -> str:
        return self.name
    
    def get_type(self) -> str:
        return self.type

    def get_description(self) -> str:
        return self.description
    
    def get_stat(self) -> int:
        return self.stat.copy()
    
    def get_stat_text(self) -> str:
        stats = self.get_stat()
        return "\n".join(f"{key.capitalize()}: {value}" for key, value in stats.items())
    
    def set_stat(self, new_stat: int) -> None:
        self.stat = new_stat.copy()

    def clone(self) -> 'GameObjects':
        return GameObjects(self.name, self.type, self.description, self.stat.copy())
    
    def set_using(self)  -> None:
        self.using = True
        
    def get_using(self) -> bool:
        return self.using
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "stat": self.stat
        }
    