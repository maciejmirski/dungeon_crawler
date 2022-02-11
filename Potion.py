from GameCharacter import GameCharacter

class Potion(GameCharacter):


    def __init__(self, symbol: str, type:str, boost:int, x:int, y:int):
        self.__symbol = symbol
        self.__type = type
        self.__boost = boost
        self.__x = x
        self.__y = y

    @property
    def symbol(self):
        return self.__symbol

    @property
    def boost(self):
        return self.__boost

    @property
    def type(self):
        return self.__type

    @boost.setter
    def boost(self, val):
        self.__boost = val

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, val):
        self.__x = val

    @y.setter
    def y(self, val):
        self.__y = val    
