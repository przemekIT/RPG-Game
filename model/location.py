class Location:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"Jesteś w: {self.name}"


class Forest(Location):
    def __init__(self):
        super().__init__("Las")


class Castle(Location):
    def __init__(self):
        super().__init__("Zamek")


class Village(Location):
    def __init__(self):
        super().__init__("Wioska")
