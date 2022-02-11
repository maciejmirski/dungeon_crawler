class Board:

    def __init__(self, board_file: str):
        self.__height = None
        self.__width = None
        self.__board_file = board_file
        self.__map = {}


    def read_board(self):
        with open(self.__board_file, 'r') as f:

            lines = f.readlines()

            self.__width = max([len(line.split(',')) for line in lines]) 

            for i, line in enumerate(lines):
                self.__map[i] = line.split(',')

            self.__height = len(self.__map)  

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def map(self):
        return self.__map        

    @property
    def board_file(self):
        return self.__board_file
