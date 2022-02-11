class GameCharacter:

    def __init__(self, symbol: str):
        self.__symbol = symbol

    @property
    def symbol(self):
        return self.__symbol
    
    @symbol.setter
    def symbol(self, val):
        self.__symbol = val