from GameCharacter import GameCharacter

class Diamond(GameCharacter):


    def __init__(self, symbol: str, type:str, points:int, x:int, y:int):
        self.__symbol = symbol
        self.__type = type
        self.__points = points
        self.__x = x
        self.__y = y

    @property
    def symbol(self):
        return self.__symbol

    @property
    def points(self):
        return self.__points

    @property
    def type(self):
        return self.__type

    @points.setter
    def points(self, val):
        self.__points = val

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
