from model.npc import NPC


class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Village(Location):
    def __init__(self):
        super().__init__("Wioska", "Spokojna wioska z kilkoma chatkami i targiem.")
        # self.npc = NPC("Starzec", "Witaj, podróżniku! Szukasz przygód?")
        self.npc = NPC(
            "Starzec",
            [
                (
                    "Szukam przygód.",
                    "Wyrusz na północny wschód – tam widziano potwory.",
                ),
                ("Kim jesteś?", "Jestem starym mędrcem, który widział niejedno."),
                ("Czy masz coś dla mnie?", "Weź tę miksturę – może ci się przyda."),
            ], can_give_items=True
        )


class Forest(Location):
    def __init__(self):
        super().__init__("Las", "Gęsty las pełen tajemniczych dźwięków i potworów.")
        # self.npc = NPC("Druid", "Czujesz to? Las przemawia do tych, którzy potrafią słuchać. Za trzy dni nadejdzie coś wielkiego...")
        self.npc = NPC(
            "Druid",
            [
                ("Kim jesteś?", "Jestem opiekunem tego lasu."),
                ("Co tu się dzieje?", "Las coś przeczuwa..."),
                ("Masz dla mnie jakąś radę?", "Słuchaj uważnie szeptów drzew."),
            ], can_give_items=True
        )


class Castle(Location):
    def __init__(self):
        super().__init__("Zamek", "Stary zamek z opuszczonymi salami i skarbami.")
        # self.npc = NPC("Strażnik", "Witaj, podróżniku! Na północy czyhają niebezpieczeństwa.")
        self.npc = NPC(
            "Strażnik",
            [
                (
                    "Czy zamek jest bezpieczny?",
                    "Od lat nikt tu nie mieszka. Ale coś się czai w ciemnościach.",
                ),
                (
                    "Co pilnujesz?",
                    "Ten zamek kryje skarb – nie każdy powinien go znaleźć.",
                ),
                ("Masz jakąś radę?", "Nie ufaj nikomu w czarnym płaszczu."),
            ], can_give_items=True
        )
