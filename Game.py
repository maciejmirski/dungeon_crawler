from tkinter import *
import random
import time
from PIL import ImageTk,Image
from GameCharacter import GameCharacter
from Enemy import Enemy
from Hero import Hero
from Board import Board 
from Sword import Sword
from Potion import Potion
from Diamond import Diamond
from tkinter import messagebox


BLUE_COLOR = "#0492CF"
HERO_ICON = 'icons/knight.png'

#Level 1
WALL_ICON = 'icons/wall_1.png'
ZOMBIE_ICON = 'icons/zombie.png'
CTHULHU_ICON = 'icons/cthulhu.png'
YOG_SOTHOTH_ICON = 'icons/final_boss.png'
BOSS_ICON = 'icons/boss_1.png'

DIAMOND_ICON = 'icons/diamond_2.png'
SWORD_ICON = 'icons/swords/sword_4.png'
POTION_ICON = 'icons/potion_1.png'
HIT_ICON = 'icons/explosion.png'

#Level 2
BUSH_ICON = 'icons/bush.png'
GRASS_ICON = 'icons/grass.png'
DROUGHT_ICON = 'icons/drought.png'
MONSTER_MUD_ICON = 'icons/monster_mud.png'
MONSTER_EYE_ICON = 'icons/monster_one_eye.png'
MONSTER_TREE_ICON = 'icons/monster_tree2.png'
BOSS_2_ICON = 'icons/boss_2.png'


GREEN_COLOR = "#7BC043"
RED_COLOR = "#EE4035"
BLACK_COLOR = "#000000"

DELAY = 10
cell_size = 40


class Game:

    wall_symbol = GREEN_COLOR 

    def __init__(self):
        self.text_freepik = None
        self.points_hud = None
        self.swords_hud = None
        self.health_hud = None
        self.text = None
        self.board_canvas = None
        self.status_panel_y = None
        self.size_of_board_y = None
        self.size_of_board_x = None
        self.board = None
        self.window = None
        self.canvas = None
        self.set_up_board_and_size("boards/board.csv")
        self.allocate_images()
        self.board_walls = []
        self.enemy_rects = {}
        self.item_rects = {}
        self.hero_rect = None
        self.hero = None
        self.crashed = False
        self.if_fog_of_war = False
        self.current_fog = None
        self.window.bind("<Key>", self.key_input)
        self.play_again()
        self.begin = False
        self.hit = False

    def all_children (self, window):
        _list = window.winfo_children()

        for item in _list :
            if item.winfo_children() :
                _list.extend(item.winfo_children())

        return _list

    def set_up_board_and_size(self, board_file:str):
        if self.window:
            widget_list = self.all_children(self.window)
            for item in widget_list:
                item.pack_forget()
            self.board_walls = []
            self.enemy_rects = {}
            self.item_rects = {}

        else:
            self.window = Tk()        
            self.window.title("Dungeon Crawler")

        self.board = Board(board_file)
        self.board.read_board()
        self.size_of_board_x = (self.board.width*cell_size)
        self.size_of_board_y = (self.board.height*cell_size)
        self.status_panel_y = self.size_of_board_y/6
        self.canvas = Canvas(self.window, width=self.size_of_board_x, height=self.size_of_board_y+self.status_panel_y)
        self.canvas.pack()

    def initialize_board(self):
        self.board_canvas = []

        for i in range(self.board.height):
            for j in range(self.board.width):
                self.board_canvas.append((i, j))

        for i in range(self.board.width):
            self.canvas.create_line(
                i * self.size_of_board_y / self.board.height, 0, i * self.size_of_board_y / self.board.height, self.size_of_board_y,
            )

        for i in range(self.board.height):
            self.canvas.create_line(
                0, i * self.size_of_board_x / self.board.width, self.size_of_board_x, i * self.size_of_board_x / self.board.width,
            )

        

    def paint_walls(self):

        for i in range(self.board.height):
            for j in range(self.board.width):
                x1 = j * cell_size
                y1 = i * cell_size

                icon = None
                conc_image = None
                if self.board.map[i][j] == 'O' or self.board.map[i][j] == 'O\n':
                    conc_image = self.wall_icon
                elif self.board.map[i][j] == '1' or self.board.map[i][j] == '1\n':
                    icon = BUSH_ICON
                elif self.board.map[i][j] == '2' or self.board.map[i][j] == '2\n':
                    icon = GRASS_ICON
                elif self.board.map[i][j] == '3' or self.board.map[i][j] == '3\n':
                    icon = DROUGHT_ICON
                else:
                    icon = None

                if icon:
                    resize_img = Image.open(icon).resize((cell_size, cell_size))
                    img = ImageTk.PhotoImage(resize_img)
                    label = Label(image=img)
                    label.image = img

                    self.board_walls.append(self.canvas.create_image(
                            x1, y1, anchor = NW, image = img    
                        )
                    )
                elif conc_image:
                    label = Label(image=conc_image)
                    label.image = conc_image

                    self.board_walls.append(self.canvas.create_image(
                            x1, y1, anchor = NW, image = conc_image
                        )
                    )

    def initialize_enemies(self):

        for i in range(self.board.height):
            for j in range(self.board.width):

                if (self.board.map[i][j] == 'Z'):
                    self.initialize_enemy(i,j,"Zombie")
                elif(self.board.map[i][j] == 'X'):
                    self.initialize_enemy(i,j,"Cthulhu")
                elif(self.board.map[i][j] == 'Y'):
                    self.initialize_enemy(i,j,"Yog-Sothoth")
                elif(self.board.map[i][j] == 'C'):
                    self.initialize_enemy(i,j,"Mud Monster")
                elif(self.board.map[i][j] == 'V'):
                    self.initialize_enemy(i,j,"Tree Monster")
                elif(self.board.map[i][j] == 'N'):
                    self.initialize_enemy(i,j,"Beholder")

                elif(self.board.map[i][j] == 'B'):
                    self.initialize_enemy(i,j,"Boss")
                elif(self.board.map[i][j] == 'b'):
                    self.initialize_enemy(i,j,"Boss 2")

                elif(self.board.map[i][j] == 'S'):
                    self.initialize_item(i,j,"Sword")
                elif(self.board.map[i][j] == 'P'):
                    self.initialize_item(i,j,"Potion")
                elif(self.board.map[i][j] == 'D'):
                    self.initialize_item(i,j,"Diamond")


    def initialize_enemy(self, y:int, x:int, type:str):
        if (type == 'Zombie'):
            enemy = Enemy(ZOMBIE_ICON, type, 10, x, y,10)
        elif (type == 'Mud Monster'):
            enemy = Enemy(MONSTER_MUD_ICON, type, 10, x, y, 10)
        elif (type == 'Cthulhu'):
            enemy = Enemy(CTHULHU_ICON, type, 20, x, y, 15)
        elif (type == 'Tree Monster'):
            enemy = Enemy(MONSTER_TREE_ICON, type, 20, x, y, 15)
        elif (type == 'Yog-Sothoth'):
            enemy = Enemy(YOG_SOTHOTH_ICON, type, 30, x, y,20)
        elif (type == 'Beholder'):
            enemy = Enemy(MONSTER_EYE_ICON, type, 30, x, y,20)
        elif (type == 'Boss'):
            enemy = Enemy(BOSS_ICON, type, 50, x, y,25)
        elif (type == 'Boss 2'):
            enemy = Enemy(BOSS_2_ICON, type, 50, x, y,25)
        else:
            enemy = Enemy(ZOMBIE_ICON, type, 10, x, y,10)

        x1 = x * cell_size + 1
        y1 = y * cell_size + 1


        resize_img = Image.open(enemy.symbol).resize((cell_size-2, cell_size-2))
        img = ImageTk.PhotoImage(resize_img)
        label = Label(image=img)
        label.image = img

        enemy_rect = self.canvas.create_image(
                x1, y1, anchor = NW, image = img    
        )
        self.enemy_rects[enemy_rect] = enemy
        

    def initialize_item(self, y:int, x:int, type:str):

        if (type == 'Sword'):
            item = Sword(SWORD_ICON, type, self.hero.sword.power+2, x, y)
        elif (type == 'Potion'):
            item = Potion(POTION_ICON, type, 10, x, y)
        else:
            item = Diamond(DIAMOND_ICON, type, 1, x, y)

        x1 = x * cell_size + 1
        y1 = y * cell_size + 1


        resize_img = Image.open(item.symbol).resize((cell_size-2, cell_size-2))
        img = ImageTk.PhotoImage(resize_img)
        label = Label(image=img)
        label.image = img

        
        item_rect = self.canvas.create_image(
                x1, y1, anchor = NW, image = img    
        )
        self.item_rects[item_rect] = item

    def initialize_hero(self):
        if not self.hero: 
            self.hero = Hero(HERO_ICON, 'Hero Name', 'Knight', 100)
        else:
            self.hero.x = 2
            self.hero.y = 2
            self.hero.health = 100
        self.crashed = False
        x1 = self.hero.x * cell_size + 1
        y1 = self.hero.y * cell_size + 1

        resize_img = Image.open(self.hero.symbol).resize((cell_size - 2, cell_size -2))
        img = ImageTk.PhotoImage(resize_img)
        label = Label(image=img)
        label.image = img

        self.hero_rect = self.canvas.create_image(
            x1, y1, anchor = NW, image = img    
        )

    def initialize_health_hud(self):
        x1 = self.size_of_board_x*0.4
        y1 = self.size_of_board_y+2
        self.canvas.create_rectangle(x1, 
            y1, 
            0.6*self.size_of_board_x,
            y1+cell_size)
        resize_img = Image.open(POTION_ICON).resize((cell_size-2, cell_size-2))
        img = ImageTk.PhotoImage(resize_img)
        label = Label(image=img)
        label.image = img
        self.canvas.create_image(
                x1, y1, anchor = NW, image = img    
        
        )
        self.health_hud = self.canvas.create_text(
            x1+cell_size+cell_size,
            y1+cell_size/2,
            font="cmr 20 bold",
            fill=BLACK_COLOR,
            text=self.hero.health,
        )

    def initialize_points_hud(self):
        x1 = self.size_of_board_x*0.6
        y1 = self.size_of_board_y+2
        self.canvas.create_rectangle(x1, 
            y1, 
            0.8*self.size_of_board_x,
            y1+cell_size)
        resize_img = Image.open(DIAMOND_ICON).resize((cell_size-2, cell_size-2))
        img = ImageTk.PhotoImage(resize_img)
        label = Label(image=img)
        label.image = img
        self.canvas.create_image(
                x1, y1, anchor = NW, image = img    
        
        )
        self.points_hud = self.canvas.create_text(
            x1+cell_size+cell_size,
            y1+cell_size/2,
            font="cmr 20 bold",
            fill=BLACK_COLOR,
            text=self.hero.points,
        )


    def initialize_sword_hud(self):
        x1 = self.size_of_board_x*0.8
        y1 = self.size_of_board_y+2
        self.canvas.create_rectangle(x1, 
            y1, 
            self.size_of_board_x,
            y1+cell_size)
        resize_img = Image.open(SWORD_ICON).resize((cell_size-2, cell_size-2))
        img = ImageTk.PhotoImage(resize_img)
        label = Label(image=img)
        label.image = img
        self.canvas.create_image(
                x1, y1, anchor = NW, image = img    
        
        )
        self.swords_hud = self.canvas.create_text(
            x1+cell_size+cell_size,
            y1+cell_size/2,
            font="cmr 20 bold",
            fill=BLACK_COLOR,
            text=f"+{self.hero.sword.power}",
        )


    def initialize_hud(self):
        self.initialize_health_hud()
        self.initialize_points_hud()
        self.initialize_sword_hud()
        self.text = self.canvas.create_text(
            self.size_of_board_x/8,
            self.size_of_board_y+2,
            font="cmr 15 bold",
            fill=BLACK_COLOR,
            justify=CENTER,
            anchor=S,
            text="",
        )
        self.text_freepik = self.canvas.create_text(
            self.size_of_board_x*0.4,
            self.size_of_board_y+70,
            font="cmr 10 bold",
            fill=BLACK_COLOR,
            justify=RIGHT,
            anchor=W,
            text='Icons made by Freepik (https://www.freepik.com) from https://www.flaticon.com/',
        )


    def update_health_hud(self):
        x1 = self.size_of_board_x*0.4
        y1 = self.size_of_board_y+2

        self.canvas.delete(self.health_hud)
        self.health_hud = self.canvas.create_text(
            x1+cell_size+cell_size,
            y1+cell_size/2,
            font="cmr 20 bold",
            fill=BLACK_COLOR,
            text=self.hero.health,
        )

    def update_points_hud(self):
        x1 = self.size_of_board_x*0.6
        y1 = self.size_of_board_y+2

        self.canvas.delete(self.points_hud)
        self.points_hud = self.canvas.create_text(
            x1+cell_size+cell_size,
            y1+cell_size/2,
            font="cmr 20 bold",
            fill=BLACK_COLOR,
            text=self.hero.points,
        )

    def update_swords_hud(self):
        x1 = self.size_of_board_x*0.8
        y1 = self.size_of_board_y+2

        self.canvas.delete(self.swords_hud)
        self.swords_hud = self.canvas.create_text(
            x1+cell_size+cell_size,
            y1+cell_size/2,
            font="cmr 20 bold",
            fill=BLACK_COLOR,
            text=f"+{self.hero.sword.power}",
        )



    def play_again(self):
        self.window.unbind("<Button-1>")
        self.canvas.delete("all")
        # msgbox = messagebox.askyesno(title="Fog of war", message="Do you want to play with fog of war?")
        # if msgbox:
        #     self.if_fog_of_war = True
        # else:
        #     self.if_fog_of_war = False
        self.initialize_board()
        self.paint_walls()
        self.initialize_hero()
        self.initialize_enemies()
        self.initialize_hud()
        self.crashed=False
        self.begin=True
        if self.if_fog_of_war:
            self.fog_of_war()
        #self.begin_time = time.time()

    def mainloop(self):
        while True:
            self.window.update()
            if self.begin:
                if not self.crashed:
                    if not self.hit:
                        self.window.after(DELAY, self.update_hero(self.last_key))

                else:
                    self.begin = False


    def check_if_key_valid(self, key):
        valid_keys = ["Up", "Down", "Left", "Right"]
        if key in valid_keys:
            return True
        else:
            return False

    def key_input(self, event):
        if not self.crashed:
            key_pressed = event.keysym
            # Check if the pressed key is a valid key
            if self.check_if_key_valid(key_pressed):
                # print(key_pressed)
                self.begin = True
                self.last_key = key_pressed

    def allocate_images(self):
        tmp_hit_icon = Image.open(HIT_ICON).resize((cell_size - 2, cell_size - 2))
        self.hit_icon = ImageTk.PhotoImage(tmp_hit_icon)

        tmp_wall_icon = Image.open(WALL_ICON).resize((cell_size, cell_size))
        self.wall_icon = ImageTk.PhotoImage(tmp_wall_icon)

    def draw_hit(self, x, y, message):
        label = Label(image=self.hit_icon)
        label.image = self.hit_icon
        image = self.canvas.create_image(
            x, y, anchor = NW, image = self.hit_icon
        
        )
        text = self.canvas.create_text(
            x+cell_size/2, y+cell_size/2-3, text=message, fill=RED_COLOR
        )
        self.hit = True
        self.canvas.after(500, self.canvas.delete, text)
        self.canvas.after(500, self.canvas.delete, image)
        self.canvas.after(500, self.set_hit, False)


    def set_hit(self, val: bool):
        self.hit = val

    def run_attack(self, enemy_in_fight):
        
        enemy = self.enemy_rects[enemy_in_fight]

        your_attack = random.randint(0, 20+self.hero.sword.power)
        enemy_health = enemy.health
        enemy.health = int(enemy_health) - your_attack 
        coords = self.canvas.coords(enemy_in_fight)
        self.draw_hit(coords[0], coords[1], f"-{your_attack}")
        
        if enemy.health <= 0:        
            message = f"{enemy.type} killed."

            self.canvas.delete(enemy_in_fight)
            self.enemy_rects.pop(enemy_in_fight)

            if enemy.type == 'Boss' or enemy.type == 'Boss 2':
                if self.board.board_file == 'board.csv':
                    message = f"You killed the Boss!\nClick to play next board"
                    self.crashed = True
                    msgbox = messagebox.showinfo(message=message)
                    if msgbox == 'ok':
                        self.set_up_board_and_size("boards/board_2.csv")
                        self.crashed = True
                        self.play_again()
                else:
                    message = f"You killed the final Boss!\nClick to start again"
                    self.crashed = True
                    msgbox = messagebox.showinfo(message=message)
                    if msgbox == 'ok':
                        self.set_up_board_and_size("board.csv")
                        self.crashed = True
                        self.play_again()

            else:
                self.update_hud(message)

        elif enemy.health > 0:
            message = f"Your attack caused: {your_attack} damage.\n{enemy.type} has: {enemy.health} health"
        
            enemy_attack = random.randint(0, enemy.damage)
            your_health = self.hero.health
            self.hero.health = int(your_health) - enemy_attack

            if self.hero.health <= 0:
                message = f"You died. Click to play again"
                self.crashed = True
                msgbox = messagebox.showinfo(message=message)
                if msgbox == 'ok':
                    self.set_up_board_and_size("board.csv")
                    self.crashed = True
                    self.play_again()

            elif self.hero.health > 0:
                coords = self.canvas.coords(self.hero_rect)
                self.canvas.after(500, self.draw_hit, coords[0], coords[1], f"-{enemy_attack}")
                message += f"\n{enemy.type} attack caused: {enemy_attack} damage."
                self.canvas.after(500, self.update_hud, message)

        self.update_health_hud()

    def pickup_item(self, item_to_be_picked_up: GameCharacter):
        item = self.item_rects[item_to_be_picked_up]

        if item.__class__ == Diamond:
            self.hero.points = 1
            self.update_points_hud()
            self.canvas.delete(item_to_be_picked_up)
            self.item_rects.pop(item_to_be_picked_up)

        elif item.__class__ == Sword:
            self.hero.sword = item
            self.update_hud(f'You have new sword!\nI has +{self.hero.sword.power} power')
            self.update_swords_hud()
            self.canvas.delete(item_to_be_picked_up)
            self.item_rects.pop(item_to_be_picked_up)

        elif item.__class__ == Potion:
            self.hero.potions = item
            self.hero.drink_potion()
            self.update_health_hud()
            self.canvas.delete(item_to_be_picked_up)
            self.item_rects.pop(item_to_be_picked_up)


    def update_hud(self, message:str):
        self.canvas.delete(self.text)
        self.text = self.canvas.create_text(
            10,
            self.size_of_board_y+10,
            font="cmr 12 bold",
            fill=BLACK_COLOR,
            justify=LEFT,
            text=message,
            anchor=NW,
            width=(self.size_of_board_x/2)-10
        )


    def fog_of_war(self):

        size_of_fog = 6
        hero_x_start = (self.hero.x-(size_of_fog/2)+0.5)*cell_size
        hero_y_start = (self.hero.y-(size_of_fog/2)+0.5)*cell_size
        hero_x_width_tmp = hero_x_start + (cell_size*size_of_fog)
        hero_y_width_tmp = hero_y_start + (cell_size*size_of_fog)
        hero_x_width = min(hero_x_width_tmp, self.size_of_board_x)
        hero_y_width = min(hero_y_width_tmp, self.size_of_board_y)

        if self.current_fog:
            self.canvas.delete(self.current_fog)
            self.current_fog = self.canvas.create_polygon(0,0,
                        self.size_of_board_x,0,
                        self.size_of_board_x,self.size_of_board_y,
                        0,self.size_of_board_y,
                        0,self.size_of_board_y/2,
                        hero_x_start, hero_y_start,
                        hero_x_width, hero_y_start,
                        hero_x_width, hero_y_width,
                        hero_x_start, hero_y_width,
                        hero_x_start, hero_y_start,
                        0,self.size_of_board_y/2,
                        0,0
                        )

        else:
            self.current_fog = self.canvas.create_polygon(0,0,
                        self.size_of_board_x,0,
                        self.size_of_board_x,self.size_of_board_y,
                        0,self.size_of_board_y,
                        0,self.size_of_board_y/2,
                        hero_x_start, hero_y_start,
                        hero_x_width, hero_y_start,
                        hero_x_width, hero_y_width,
                        hero_x_start, hero_y_width,
                        hero_x_start, hero_y_start,
                        0,self.size_of_board_y/2,
                        0,0
                        )

    def update_hero(self, key):

        new_x = self.hero.x
        new_y = self.hero.y

        if key == "Left":
            new_x = self.hero.x-1
            new_y = self.hero.y
        elif key == "Right":
            new_x = self.hero.x+1
            new_y = self.hero.y
        elif key == "Up":
            new_x = self.hero.x
            new_y = self.hero.y-1
        elif key == "Down":
            new_x = self.hero.x
            new_y = self.hero.y+1

        if key:
            x1 = new_x * cell_size + 1
            y1 = new_y * cell_size + 1
            x2 = x1 + cell_size - 2
            y2 = y1 + cell_size - 2

            overlap = False
            overlap_attack = False
            overlap_item = False

            for wall in self.board_walls:
                if wall in self.canvas.find_overlapping(x1, y1, x2, y2):
                    overlap = True

            for enemy_rect in self.enemy_rects:
                if enemy_rect in self.canvas.find_overlapping(x1, y1, x2, y2):
                    overlap_attack = True
                    enemy_in_fight = enemy_rect

            for item_rect in self.item_rects:
                if item_rect in self.canvas.find_overlapping(x1, y1, x2, y2):
                    overlap_item = True
                    item_to_be_picked_up = item_rect

            if (overlap == False) and (overlap_attack == False):
                self.canvas.delete(self.hero_rect)
                resize_img = Image.open(self.hero.symbol).resize((cell_size - 2, cell_size - 2))
                img = ImageTk.PhotoImage(resize_img)
                label = Label(image=img)
                label.image = img

                if overlap_item:
                    self.pickup_item(item_to_be_picked_up)


                self.hero_rect = self.canvas.create_image(
                    x1, y1, anchor = NW, image = img
                )

                self.hero.x = new_x
                self.hero.y = new_y
                if self.if_fog_of_war:
                    self.fog_of_war()

            elif (overlap == False) and (overlap_attack == True):
                self.run_attack(enemy_in_fight)


            self.last_key = None




g = Game()
g.mainloop()
