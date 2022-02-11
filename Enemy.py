from GameCharacter import GameCharacter

class Enemy(GameCharacter):


    def __init__(self, symbol: str, type:str, health:int, x:int, y:int, damage: int = None):
        self.__symbol = symbol
        self.__type = type
        self.__health = health
        self.__x = x
        self.__y = y
        self.__damage = damage

    @property
    def symbol(self):
        return self.__symbol

    @property
    def health(self):
        return self.__health

    @property
    def type(self):
        return self.__type

    @health.setter
    def health(self, val):
        self.__health = val

    @property
    def damage(self):
        return self.__damage

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

    @damage.setter
    def damage(self, val):
        self.__damage = val    
