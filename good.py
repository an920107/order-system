class Good:
    def __init__(self, *, name: str, price: int, fat: int):
        self.name = str(name)
        self.price = int(price)
        self.fat = int(fat)

    def __repr__(self):
        return str(self.__dict__)
    
    def __hash__(self):
        return hash(self.name)
