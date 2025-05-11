from model.npc import NPC

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Village(Location):
    def __init__(self):
        super().__init__("Wioska", "Spokojna wioska z kilkoma chatkami i targiem.")
        self.npc = NPC(
            "Starzec",
            [
                ("Kim jesteś?", "Jestem starym mędrcem, który widział niejedno."),
                (
                    "Czy znasz jakieś sekrety tych terenów?",
                    "Mówią, że w ruinach starej wieży kryje się coś, co nie powinno ujrzeć światła dziennego.",
                ),
                (
                    "Potrzebuję rady.",
                    "Nie każda walka jest warta stoczenia. Czasem mądrość tkwi w odwrocie.",
                ),
            ],
            can_give_items=True,
        )


class Forest(Location):
    def __init__(self):
        super().__init__("Las", "Gęsty las pełen tajemniczych dźwięków i potworów.")
        self.npc = NPC(
            "Druid",
            [
                ("Kim jesteś?", "Jestem opiekunem tego lasu."),
                ("Co tu się dzieje?", "Las coś przeczuwa..."),
                ("Masz dla mnie jakąś radę?", "Słuchaj uważnie szeptów drzew."),
            ],
            can_give_items=True,
        )


class Castle(Location):
    def __init__(self):
        super().__init__("Zamek", "Stary zamek z opuszczonymi salami i skarbami.")
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
            ],
            can_give_items=True,
        )
