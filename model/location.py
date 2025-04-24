# class Location:
#     def __init__(self, name):
#         self.name = name

#     def describe(self):
#         return f"Jesteś w: {self.name}"


# class Forest(Location):
#     def __init__(self):
#         super().__init__("Las")


# class Castle(Location):
#     def __init__(self):
#         super().__init__("Zamek")


# class Village(Location):
#     def __init__(self):
#         super().__init__("Wioska")

from model.npc import NPC

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Village(Location):
    def __init__(self):
        super().__init__("Wioska", "Spokojna wioska z kilkoma chatkami i targiem.")
        self.npc = NPC("Starzec", "Witaj, podróżniku! Szukasz przygód?")

class Forest(Location):
    def __init__(self):
        super().__init__("Las", "Gęsty las pełen tajemniczych dźwięków i potworów.")

class Castle(Location):
    def __init__(self):
        super().__init__("Zamek", "Stary zamek z opuszczonymi salami i skarbami.")