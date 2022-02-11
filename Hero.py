from typing import List
from GameCharacter import GameCharacter
from Sword import Sword
from Potion import Potion

class Hero(GameCharacter):

    start_x = 2
    start_y = 2

    def __init__(self, symbol: str, name: str, char_class:str, health:int, sword:Sword = None, potions:List[Potion] = []):
        self.__symbol = symbol
        self.__name = name
        self.__char_class = char_class
        self.__health = health
        self.__x = self.start_x
        self.__y = self.start_y
        if sword == None:
            self.__sword = Sword(None,"Basic",5,None,None)
        self.__potions = potions
        self.__points = 0


    @property
    def symbol(self):
        return self.__symbol

    @property
    def health(self):
        return self.__health

    @property
    def name(self):
        return self.__name

    @property
    def char_class(self):
        return self.__char_class

    @health.setter
    def health(self, val):
        self.__health = val

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

    @property
    def sword(self):
        return self.__sword

    @sword.setter    
    def sword(self, val: Sword):
        self.__sword = val

    @property
    def points(self):
        return self.__points

    @points.setter    
    def points(self, val: int):
        self.__points += val

    @property
    def potions(self):
        return self.__potions

    @potions.setter    
    def potions(self, val: Potion):
        self.__potions.append(val)

    def drink_potion(self):
        p = self.__potions.pop()
        self.health = self.__health + p.boost