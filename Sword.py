from GameCharacter import GameCharacter

class Sword(GameCharacter):


    def __init__(self, symbol: str, type:str, power:int, x:int, y:int):
        self.__symbol = symbol
        self.__type = type
        self.__power = power
        self.__x = x
        self.__y = y

    @property
    def symbol(self):
        return self.__symbol

    @property
    def power(self):
        return self.__power

    @property
    def type(self):
        return self.__type

    @power.setter
    def power(self, val):
        self.__power = val

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
