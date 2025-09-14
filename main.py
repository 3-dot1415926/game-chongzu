import pygame
from sys import exit
from random import randint
from math import sin,cos,radians
#from easygui import msgbox
import sys
import os
import webbrowser
from pyperclip import paste

_k=2

def encode2(game_map):#适配通道蛋白
    l = len(game_map)#该值应为已知，边长
    enlist = []#记录结果
    worldstr = []#将大列表转换为一行
    for z in range(l):
        for y in range(l):
            for x in range(l):
                worldstr.append(game_map[z][y][x])
    last = -1
    counter = -1
    for i in worldstr:
        if last == -1:
            if type(i) == str:
                enlist.append(dict1[i])
                continue
            else:
                last = i
        if last == i:
            counter += 1
        else:
            counter += 1
            enlist.append(str(counter)+str('abcdefghijk'[last]))
            counter = 0
            last = -1
        if last == -1:
            if type(i) == str:
                enlist.append(dict1[i])
                continue
            else:
                last = i
    if last != -1:
        enlist.append(str(counter)+'abcdefghijk'[last])
    return ''.join(enlist)+str(l)
def decode2(game_map_code):
    table = {'a':'0','b':'1','c':'2','d':'3','e':'4','f':'5'}
    worldsize = int(game_map_code[-1])
    if worldsize == 0:
        worldsize = int(game_map_code[-2:])
        game_map_code = game_map_code[:-2]
    else:
        game_map_code = game_map_code[:-1]
    global world_lenth
    world_lenth = int((35-worldsize)*_k)#int(35-worldsize)
    world = []
    counter0 = []
    upper_decode = []
    for i in game_map_code:
        #print(i)
        if i.isdigit():
            counter0.append(i)
            #print('digit',counter0)
        elif i.isupper():
            upper_decode.append(i)
            if len(upper_decode) == 2:
                world.append(dict2[''.join(upper_decode)])
                #print('upper,addtoworld',upper_decode)
                upper_decode = []
            #else:
            #    #print('upper',upper_decode)
        else:
            for j in int(''.join(counter0))*table[i]:
                world.append(int(j))
            counter0 = []
            #print('add',world[-1])
    #print(worldsize,'\n',world)
    st = [world[i:i+worldsize] for i in range(0, len(world), worldsize)]
    #print(st)
    st = [st[i:i+worldsize] for i in range(0, len(st), worldsize)]
    #print(st)
    return st
def get_path(path):
    if hasattr(sys,'_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path,path)

class Button():
    def __init__(self,rect,img):
        self.rect = pygame.Rect(rect)
        self.w = self.rect[2]
        self.h = self.rect[3]
        self.pos = rect[0],rect[1]
        self.pos1 = (self.rect.centerx-abs(rect[0]-self.rect.centerx)*1.2,
                     self.rect.centery-abs(rect[1]-self.rect.centery)*1.2)
        self.img0 = pygame.transform.scale(img,(rect[2],rect[3]))
        self.img1 = pygame.transform.scale(self.img0,(int(rect[2]*1.2),int(rect[3]*1.2)))
        
        self.isclick = False
        self.draw_img = self.img0
        self.draw_pos = self.pos
        self.index = None
    def move(self,newpos):
        self.pos = newpos
        self.rect = pygame.Rect(self.pos,(self.w,self.h))
        self.pos1 = (self.rect.centerx-abs(newpos[0]-self.rect.centerx)*1.2,
                     self.rect.centery-abs(newpos[1]-self.rect.centery)*1.2)
    def update(self,mousepos):
        if self.pos[0] <= mousepos[0] <= self.pos[0]+self.rect[2] and self.pos[1] <= mousepos[1] <= self.pos[1]+self.rect[3]:
            self.isclick = True
            self.draw_img = self.img1
            self.draw_pos = self.pos1
        else:
            self.isclick = False
            self.draw_img = self.img0
            self.draw_pos = self.pos
    def draw(self,screen):
        screen.blit(self.draw_img,self.draw_pos)

class Piece():
    def __init__(self,pos,group,l=2,color=(255,255,255)):
        #self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.arg = randint(180,360)
        self.v = randint(1,2)/8
        self.vx = self.v*cos(radians(self.arg))
        self.vy = self.v*sin(radians(self.arg))
        self.a = 0.05#加速度
        self.l = l
        self.color = color
        self.group = group
        self.group.append(self)
    def update(self):#玩家
        self.x += self.vx
        if self.vy<0.3:
            self.vy += self.a
        self.y += self.vy
        if self.y>600 or self.x>800 or self.x<0:
            self.group.remove(self)
            Piece((randint(1,799),-5),self.group)
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(int(self.x),int(self.y),self.l,self.l))

def main0():
    def main(level1,normal_mode=True):#若是load的关卡，normal_mode取False
        global world_lenth
        #world_lenth = 35
        maxy = 600
        class Piece():
            def __init__(self,pos,group,l=2,color=(255,255,255)):
                #self.pos = pos
                self.x = pos[0]
                self.y = pos[1]
                self.arg = randint(180,360)
                self.v = randint(1,2)/8
                self.vx = self.v*cos(radians(self.arg))
                self.vy = self.v*sin(radians(self.arg))
                self.a = 0.05#加速度
                self.l = l
                self.color = color
                self.group = group
                self.group.append(self)
            def update(self):#玩家
                self.x += self.vx
                if self.vy<0.2:
                    self.vy += self.a
                self.y += self.vy
                if self.y>maxy or self.x>600 or self.x<0:
                    self.group.remove(self)
                    Piece((randint(0,600),-5),piecegroup)
            def draw(self):
                pygame.draw.rect(screen,self.color,(int(self.x),int(self.y),self.l,self.l))
        class Piece1():
            def __init__(self,pos,l=5,color=(255,255,0)):
                #self.pos = pos
                self.x = pos[0]
                self.y = pos[1]
                self.arg = randint(180,360)
                self.v = randint(3,5)
                self.vx = self.v*cos(radians(self.arg))
                self.vy = self.v*sin(radians(self.arg))
                self.a = 1#加速度
                self.l = l
                self.color = color
            def update(self):#玩家
                self.x += self.vx
                self.vy += self.a
                self.y += self.vy
            def draw(self):
                pygame.draw.rect(screen,self.color,(int(self.x),int(self.y),self.l,self.l))
        class Up_shade():
            def __init__(self,pos,l=world_lenth,w=None,h=3,type0=0,block=None):
                self.w = l if w is None else w
                self.h = h
                self.pos = list(pos)
                self.rect = pygame.Rect(self.pos[0],self.pos[1],self.w,self.h)
                self.type0 = type0  #0-普通  1-胜利
                self.block = block
            def draw(self):
                pygame.draw.rect(screen,(255,0,0),(self.pos[0],self.pos[1],self.w,self.h))
            def move(self,x,y):
                self.pos[0]+=x
                self.pos[1]+=y
                self.rect = pygame.Rect(int(self.pos[0]),int(self.pos[1]),self.w,self.h)
        class Down_shade():
            def __init__(self,pos,l=world_lenth,w=None,h=3,type0=0,block=None):
                self.w = l-2 if w is None else w
                self.h = h
                self.pos = [pos[0]+1,pos[1]+l-h]
                self.rect = pygame.Rect(self.pos[0],self.pos[1],self.w,self.h)
                self.type0 = type0
                self.block = block
            def draw(self):
                pygame.draw.rect(screen,(0,255,0),(self.pos[0],self.pos[1],self.w,self.h))
            def move(self,x,y):
                self.pos[0]+=x
                self.pos[1]+=y
                self.rect = pygame.Rect(int(self.pos[0]),int(self.pos[1]),self.w,self.h)
        class Left_shade():
            def __init__(self,pos,l=world_lenth,w=3,h=None,type0=0,block=None):
                self.w = w
                self.h = l if h is None else h
                self.pos = list(pos)
                self.rect = pygame.Rect(self.pos[0],self.pos[1],self.w,self.h)
                self.type0 = type0
                self.block = block
            def draw(self):
                pygame.draw.rect(screen,(0,0,255),(self.pos[0],self.pos[1],self.w,self.h))
            def move(self,x,y):
                self.pos[0]+=x
                self.pos[1]+=y
                self.rect = pygame.Rect(int(self.pos[0]),int(self.pos[1]),self.w,self.h)
        class Right_shade():
            def __init__(self,pos,l=world_lenth,w=3,h=None,type0=0,block=None):
                self.w = w
                self.h = l if h is None else h
                self.pos = [pos[0]+l-w,pos[1]]
                self.rect = pygame.Rect(self.pos[0],self.pos[1],self.w,self.h)
                self.type0 = type0
                self.block = block
            def draw(self):
                pygame.draw.rect(screen,(255,0,255),(self.pos[0],self.pos[1],self.w,self.h))
            def move(self,x,y):
                self.pos[0]+=x
                self.pos[1]+=y
                self.rect = pygame.Rect(int(self.pos[0]),int(self.pos[1]),self.w,self.h)
        class Block():
            def __init__(self,pos,l=world_lenth,color=(255,255,255),space_pos=None,type0=0):
                self.color = color
                self.pos = list(pos)
                self.space_pos = space_pos
                self.l = l
                self.type0 = type0
                self.upshade = None
                self.downshade = None
                self.leftshade = None
                self.rightshade = None
                self.p1x=None
                self.p2x=None
                self.p3x=None
                self.p4x=None
                self.p1y=None
                self.p2y=None
                self.p3y=None
                self.p4y=None
            def build_shade(self):
                #print('from block',self.type0)
                self.upshade = Up_shade(self.pos,self.l,type0=self.type0,block=self)
                #print('from block upshade',self.upshade.type0)
                self.downshade = Down_shade(self.pos,self.l,block=self)
                self.leftshade = Left_shade(self.pos,self.l,block=self)
                self.rightshade = Right_shade(self.pos,self.l,block=self)
            def add_shade_to_world(self):
                world_upshade.append(self.upshade)
                world_downshade.append(self.downshade)
                world_leftshade.append(self.leftshade)
                world_rightshade.append(self.rightshade)
            def draw(self):
                if type(self.color) == tuple:
                    pygame.draw.rect(screen,self.color,(self.pos[0],self.pos[1],self.l,self.l))
                else:
                    screen.blit(pygame.transform.scale(self.color,(int(self.l),int(self.l))),(self.pos[0],self.pos[1]))
            def draw_shade(self):
                self.upshade.draw()
                self.downshade.draw()
                self.leftshade.draw()
                self.rightshade.draw()
        class Channel(Block):
            def __init__(self,pos,l=world_lenth,color=(255,255,255),space_pos=None,type0=4,faces='111111'):
                super().__init__(pos,l,color,space_pos,type0=4)
                self.faces0 = faces
                self.faces = {'fount':int(faces[0]),'back':int(faces[1]),'left':int(faces[2]),'right':int(faces[3]),'up':int(faces[4]),'down':int(faces[5])}    #1有0无
                self.fount = faces[4]+faces[2]+faces[5]+faces[3] if not faces[0] else '1'#上左下右
                self.left = faces[4]+faces[1]+faces[5]+faces[0] if not faces[2] else '1'
                self.right = faces[4]+faces[0]+faces[5]+faces[1] if not faces[3] else '1'
                self.upshades = []
                self.downshades = []
                self.leftshades = []
                self.rightshades = []
                self.img0 = self.color
                self.imgleft = None
                self.imgright = None
            def build_shade(self):#Upshade:  def __init__(self,pos,l=world_lenth,w=None,h=3,type0=0):
                if self.faces['fount']:
                    self.upshades = [Up_shade(self.pos,self.l,type0=self.type0)]
                    self.downshades = [Down_shade(self.pos,self.l,type0=self.type0)]
                    self.leftshades = [Left_shade(self.pos,self.l,type0=self.type0)]
                    self.rightshades = [Right_shade(self.pos,self.l,type0=self.type0)]
                else:
                    if self.faces['up']:
                        self.upshades.append(Up_shade(self.pos,self.l,h=1,type0=self.type0))
                        self.downshades.append(Down_shade((self.pos[0]-1,self.pos[1]-self.l+2),w=self.l,h=1,type0=self.type0))
                        self.leftshades.append(Left_shade((self.pos[0],self.pos[1]),self.l,w=1,h=2,type0=self.type0))
                        self.rightshades.append(Right_shade((self.pos[0],self.pos[1]),self.l,w=1,h=2,type0=self.type0))
                    if self.faces['left']:
                        self.upshades.append(Up_shade(self.pos,self.l,w=1,h=1,type0=self.type0))
                        self.downshades.append(Down_shade((self.pos[0]-1,self.pos[1]),self.l,w=1,h=1,type0=self.type0))
                        self.leftshades.append(Left_shade((self.pos[0],self.pos[1]),self.l,w=1,h=self.l,type0=self.type0))
                        self.rightshades.append(Right_shade((self.pos[0]-self.l,self.pos[1]),self.l,w=1,h=self.l,type0=self.type0))
                    if self.faces['right']:
                        self.upshades.append(Up_shade((self.pos[0]+self.l,self.pos[1]),self.l,w=1,h=1,type0=self.type0))
                        self.downshades.append(Down_shade((self.pos[0]+self.l-2,self.pos[1]),self.l,w=1,h=1,type0=self.type0))
                        self.leftshades.append(Left_shade((self.pos[0]+self.l,self.pos[1]),self.l,w=1,h=self.l,type0=self.type0))
                        self.rightshades.append(Right_shade((self.pos[0],self.pos[1]),self.l,w=1,h=self.l,type0=self.type0))
                    if self.faces['down']:
                        self.upshades.append(Up_shade((self.pos[0],self.pos[1]+self.l-1),self.l,h=1,type0=self.type0))
                        self.downshades.append(Down_shade((self.pos[0]-1,self.pos[1]),w=self.l,h=1,type0=self.type0))
                        self.leftshades.append(Left_shade((self.pos[0],self.pos[1]+self.l),self.l,w=1,h=1,type0=self.type0))
                        self.rightshades.append(Right_shade((self.pos[0],self.pos[1]+self.l),self.l,w=1,h=1,type0=self.type0))
            def add_shade_to_world(self):
                for i in self.upshades:
                    world_upshade.append(i)
                for i in self.downshades:
                    world_downshade.append(i)
                for i in self.leftshades:
                    world_leftshade.append(i)
                for i in self.rightshades:
                    world_rightshade.append(i)
            def update(self):
                self.fount = self.faces0[4]+self.faces0[2]+self.faces0[5]+self.faces0[3] if not int(self.faces0[0]) else '1'#上左下右
                self.left = self.faces0[4]+self.faces0[1]+self.faces0[5]+self.faces0[0] if not int(self.faces0[2]) else '1'
                self.right = self.faces0[4]+self.faces0[0]+self.faces0[5]+self.faces0[1] if not int(self.faces0[3]) else '1'
                self.color = channel_imgs[self.fount]
                self.img0 = self.color
                self.imgleft = channel_imgs[self.left]
                self.imgright = channel_imgs[self.right]
            def draw_shade(self):
                for i in self.upshades:
                    i.draw()
                for i in self.downshades:
                    i.draw()
                for i in self.leftshades:
                    i.draw()
                for i in self.rightshades:
                    i.draw()
        class Player(Block):
            def __init__(self,pos,l=int(world_lenth/2),space_pos=None):
                super().__init__(pos,l,space_pos)
                self.l = l
                self.pos = list(self.pos)
                self.space_pos = space_pos
                self.fall = True
                self.vy = 0
                self.color = (255,255,0)
                self.img1 = player1_img
                self.img2 = player2_img
                self.shades = (self.upshade,self.downshade,self.leftshade,self.rightshade)
                self.lockpos = None#用于锚点块，记录位置，采用整数坐标，x,z
                self.dirc = 1#用于绘图，记录面向的方向，0左1右
                self.can_set = False
                #self.will_set_pos = None
            def build_shade(self):
                self.upshade = Up_shade(self.pos,self.l)
                self.downshade = Down_shade(self.pos,self.l)
                self.leftshade = Left_shade(self.pos,self.l)
                self.rightshade = Right_shade(self.pos,self.l)
                self.shades = (self.upshade,self.downshade,self.leftshade,self.rightshade)
            def move1X(self,x):
                self.pos[0]+=(1 if x else -1)
                for shade in self.shades:
                    shade.move(1 if x else -1,0)
            def move1Y(self,y):
                self.pos[1]+=(1 if y else -1)
                for shade in self.shades:
                    shade.move(0,1 if y else -1)
            def check_collide(self,shade1,shade_list):
                res = shade1.rect.collidelist(shade_list)
                if res != -1:
                    if shade1==self.downshade and shade_list[res].type0 == 1:
                        return you_win()
                    elif shade1==self.downshade and shade_list==world_downshade:
                        if shade_list[res].type0 == 4:
                            for i in range(10):##########################################################################################################################
                                self.move1Y(0)
                            self.fall = True
                            return False
                        else:
                            get_return_lost = you_lost()
                            if get_return_lost == 1:
                                return 1
                            elif get_return_lost == 3:
                                return 3
                    elif shade1==self.downshade and shade_list[res].type0 == 3:
                        get_return_lost = you_lost()
                        if get_return_lost == 1:
                            return 1
                        elif get_return_lost == 3:
                            return 3
                    elif shade1==self.downshade and shade_list[res].type0 == 2:#锚点块
                        #print(1)
                        self.lock_pos = [self.space_pos[0],shade_list[res].block.space_pos[1]]
                        self.can_set = True
                        #print(self.can_set)
                    if shade1==self.downshade and shade_list[res].type0 != 2:#离开锚点块
                        self.can_set = False
                    #print(22222)
                    return True
                else:
                    return False
            def moveY(self,vy):
                set_vy_to_0 = False
                if vy<0:#向上移动
                    for i in range(int(-vy)):
                        self.move1Y(0)
                        if self.check_collide(self.upshade,world_downshade):
                            self.move1Y(1)
                            set_vy_to_0 = True
                            break
                    if set_vy_to_0:
                        self.vy=0
                else:
                    for i in range(int(vy)):
                        self.move1Y(1)
                        get_chcek_return = self.check_collide(self.downshade,world_upshade)#检测是否正常踩到地板
                        if get_chcek_return == 1 and type(get_chcek_return)==int:#如果是数字1说明寄了
                            return 1#重开
                        elif get_chcek_return == True:
                            self.move1Y(0)
                            set_vy_to_0 = True
                            self.fall = False
                            '''
                            aim_y = self.get_world_pos()[2]+1
                            for blocks in activeblock:
                                
                                if blocks.type0 == 2:#如果是锚点块，求出坐标
                                    bly = (blocks.pos[1]-basicz)//world_lenth
                                    print(bly,aim_y)
                                    if aim_y == bly:
                                        self.lock_pos = [self.space_pos[0],blocks.space_pos[1]]#self.space_pos = [self.space_pos[0],blocks.space_pos[1]]
                                        self.can_set = True
                            break
                            '''
                        elif get_chcek_return == 2:
                            return 2
                        elif get_chcek_return == 4:
                            return 4
                    if self.check_collide(self.downshade,world_downshade) == 1:
                        return 1
                    if set_vy_to_0:
                        self.vy=0
            def moveX(self,direction,step=int(3*_k*0.9)):  #direction=+-1
                #self.can_set = False
                self.fall = True
                if direction == 1:#right
                    for i in range(step):
                        self.move1X(1)
                        if self.check_collide(self.rightshade,world_leftshade):
                            self.move1X(0)
                            break
                else:
                    for i in range(step):
                        self.move1X(0)
                        if self.check_collide(self.leftshade,world_rightshade):
                            self.move1X(1)
                            break
                self.check_collide(self.downshade,world_upshade)
            def jump(self):
                if not self.fall:
                    sound0.play()
                    self.vy=int(-7*_k*0.75)
                    self.fall = True
            def get_world_pos(self):
                t = (world_arg//90)%4#0:初始；1:转90；2:转180；3:转270
                if t==0:
                    x = (self.pos[0]-basicx+self.l/2)//world_lenth
                    z = (world_lenth*world_z-self.space_pos[1]+basicz+self.l/2)//world_lenth
                elif t==1:
                    z = (world_lenth*world_z-self.space_pos[1]+basicz+self.l/2)//world_lenth
                    x = (self.pos[0]-basicx+self.l/2)//world_lenth
                elif t==2:
                    x = (self.pos[0]-basicx+self.l/2)//world_lenth
                    z = (world_lenth*world_z-self.space_pos[1]+basicz+self.l/2)//world_lenth
                elif t==3:
                    z = (world_lenth*world_w-self.space_pos[1]+basicz+self.l/2)//world_lenth
                    x = (self.pos[0]-basicx+self.l/2)//world_lenth
                y = (self.pos[1]-basicy)//world_lenth
                return x,z,y
            def update(self,gravity=0.6):
                if self.fall:
                    self.vy+=gravity
                    get_move_return = self.moveY(self.vy)
                    if get_move_return == 1:
                        return 1
                    elif get_move_return == 2:
                        return 2
                    elif get_move_return == 4:#下一关
                        return 4
                if self.pos[1]>max_y:
                    return you_lost()
            def draw(self):
                screen.blit(pygame.transform.scale(self.img1,(int(self.l),int(self.l))),(self.pos[0],self.pos[1]))
            def change_dir(self,newdirc):
                if self.dirc != newdirc:
                    self.img1 = pygame.transform.flip(self.img1, True, False)
                    self.dirc = newdirc
        def make_up_map(world_z,world_h,world_w,game_map):
            #print(game_map)
            retype = 0
            blockgroup = []
            bloakdict = {}
            world_z=world_h=world_w=len(game_map)
            for z in range(world_z):
                for y in range(world_h):
                    for x in range(world_w):
                        #print(world_w)
                        if game_map[z][y][x]==1:#基础块simple_block
                            newblock = Block((basicx+x*world_lenth,basicy+y*world_lenth),space_pos=(basicx+x*world_lenth,basicz+z*world_lenth))
                            newblock.color = block1_img
                            blockgroup.append(newblock)
                            blockdict[(x,y,z)] = newblock
                        elif game_map[z][y][x]==3:#终点win_block
                            newblock = Block((basicx+x*world_lenth,basicy+y*world_lenth),space_pos=(basicx+x*world_lenth,basicz+z*world_lenth),type0=1)
                            newblock.color = block3_img#(255,155,0)
                            blockgroup.append(newblock)
                            blockdict[(x,y,z)] = newblock
                        elif game_map[z][y][x]==2:#玩家
                            player0 = Player([basicx+x*world_lenth+int(0.1*world_lenth),basicy+y*world_lenth],space_pos=[basicx+x*world_lenth+int(0.1*world_lenth),basicz+z*world_lenth+int(0.1*world_lenth)])
                            player0.build_shade()
                            retype = 1
                        elif game_map[z][y][x]==4:#锚点方块stuck_block
                            newblock = Block((basicx+x*world_lenth,basicy+y*world_lenth),space_pos=(basicx+x*world_lenth,basicz+z*world_lenth),type0=2)
                            newblock.color = block2_img#(0,155,0)
                            blockgroup.append(newblock)
                            blockdict[(x,y,z)] = newblock
                        elif game_map[z][y][x]==5:#寄块re_block
                            newblock = Block((basicx+x*world_lenth,basicy+y*world_lenth),space_pos=(basicx+x*world_lenth,basicz+z*world_lenth),type0=3)
                            newblock.color = block4_img
                            blockgroup.append(newblock)
                            blockdict[(x,y,z)] = newblock
                        elif type(game_map[z][y][x]) == str:#通道蛋白channel
                            newblock = Channel((basicx+x*world_lenth,basicy+y*world_lenth),space_pos=(basicx+x*world_lenth,basicz+z*world_lenth),type0=4,faces=game_map[z][y][x])
                            newblock.update()
                            blockgroup.append(newblock)
                            blockdict[(x,y,z)] = newblock
            blocklist_with_z = []
            for i in range(world_z+1):
                blocklist_with_z.append([])
            for i in blockgroup:
                blocklist_with_z[world_w-int((i.space_pos[1]-basicx)/(20*_k))].append(i)
            activeblock = []
            for x in range(world_w):
                for y in range(world_h):
                    for z in range(world_z-1,-1,-1):
                        if game_map[z][y][x] != 0 and game_map[z][y][x] != 2:
                            blockdict[(x,y,z)].build_shade()
                            blockdict[(x,y,z)].add_shade_to_world()
                            activeblock.append(blockdict[(x,y,z)])
                            break
            if retype == 1:
                return activeblock,blockgroup,blockdict,blocklist_with_z,player0
            else:
                return activeblock,blockgroup,blockdict,blocklist_with_z
        def turn_1(blockgroup,game_map):#顺时针转动
            drawlist = []#创建画图顺序列表
            playerx,playerz,playery = player.get_world_pos()
            if playerx<0:
                drawlist.append(player)
            for x in range(world_w):
                if x==playerx and playery>world_h and not player in drawlist:
                    drawlist.append(player)
                for y in range(world_h):
                    for z in range(world_z):
                        if x==playerx and y==playery:#检查player是否已在drawlist中，没有则加入，保持玩家正常被遮挡
                            if playerz<0 or z==playerz or (not player in drawlist and z==0):
                                drawlist.append(player)
                        if game_map[z][y][x] == 1 or game_map[z][y][x] == 3 or game_map[z][y][x] == 4 or game_map[z][y][x] == 5 or type(game_map[z][y][x])==str:#将普通块加入
                            drawlist.append(blockdict[(x,y,z)])
            if not(player in drawlist):
                drawlist.append(player)
            centerx,centery = basicx+world_lenth*world_w/2,basicy+world_lenth*world_z/2#计算和画图
            for block in blockgroup:
                block.p1x,block.p1y = block.space_pos[0],block.space_pos[1]                                     #p1—p2
                block.p2x,block.p2y = block.space_pos[0]+world_lenth,block.space_pos[1]                         # |  |
                block.p3x,block.p3y = block.space_pos[0]+world_lenth,block.space_pos[1]+world_lenth             #p4—p3
                block.p4x,block.p4y = block.space_pos[0],block.space_pos[1]+world_lenth                         #
            player.p1x,player.p1y = player.pos[0],player.space_pos[1]
            player.p2x,player.p2y = player.pos[0]+player.l,player.space_pos[1]
            player.p3x,player.p3y = player.pos[0]+player.l,player.space_pos[1]+player.l
            player.p4x,player.p4y = player.pos[0],player.space_pos[1]+player.l
            for arg in range(0,90,1):#range(world_arg,world_arg+90,1):#range(90,0,-1):
                pygame.event.get()
                screen.fill((0,0,0))
                for piece in piecegroup:#粒子效果
                    piece.x += 1
                    if piece.x>600:
                        piece.x = 0
                    pygame.draw.rect(screen,piece.color,(int(piece.x),int(piece.y),piece.l,piece.l))
                for block in drawlist:
                    if block!=player:
                        p1x1 = (block.p1x-centerx)*cos(radians(arg))-(block.p1y-centery)*sin(radians(arg))+centerx
                        p2x1 = (block.p2x-centerx)*cos(radians(arg))-(block.p2y-centery)*sin(radians(arg))+centerx
                        p3x1 = (block.p3x-centerx)*cos(radians(arg))-(block.p3y-centery)*sin(radians(arg))+centerx
                        p4x1 = (block.p4x-centerx)*cos(radians(arg))-(block.p4y-centery)*sin(radians(arg))+centerx
                        if type(block.color) == tuple:
                            pygame.draw.rect(screen,block.color,(p3x1,block.pos[1],p4x1-p1x1,world_lenth))
                        else:
                            if block.type0 == 4:
                                newimg = pygame.transform.scale(block.imgright,(abs(int(p3x1-p2x1)),world_lenth))
                                screen.blit(newimg,(p3x1,block.pos[1]))
                                newimg = pygame.transform.scale(block.img0,(int(p3x1-p4x1)+1,world_lenth))
                                screen.blit(newimg,(p4x1,block.pos[1]))
                            else:
                                newimg = pygame.transform.scale(block.color,(abs(int(p3x1-p2x1)),world_lenth))
                                screen.blit(newimg,(p3x1,block.pos[1]))
                                newimg = pygame.transform.scale(block.color,(int(p3x1-p4x1)+1,world_lenth))
                                screen.blit(newimg,(p4x1,block.pos[1]))
                    else:
                        player_p1x1 = (player.p1x-centerx)*cos(radians(arg))-(player.p1y-centery)*sin(radians(arg))+centerx
                        player_p2x1 = (player.p2x-centerx)*cos(radians(arg))-(player.p2y-centery)*sin(radians(arg))+centerx
                        player_p3x1 = (player.p3x-centerx)*cos(radians(arg))-(player.p3y-centery)*sin(radians(arg))+centerx
                        player_p4x1 = (player.p4x-centerx)*cos(radians(arg))-(player.p4y-centery)*sin(radians(arg))+centerx
                        player_p4y1 = (player.p4y-centery)*cos(radians(arg))+(player.p4x-centery)*sin(radians(arg))+centery
                        player.space_pos = [player_p4x1,player_p4y1]
                        player.pos = [player_p4x1,player.pos[1]]
                        newimg = pygame.transform.scale(player.img2,(abs(int(player_p3x1-player_p2x1)),int(world_lenth/2)))
                        screen.blit(newimg,(player_p3x1,block.pos[1]))
                        newimg = pygame.transform.scale(player.img2,(int(player_p3x1-player_p4x1)+1,int(world_lenth/2)))
                        screen.blit(newimg,(player_p4x1,block.pos[1]))
                new1surface = screen.subsurface((0, 0, 600, 600)).copy()
                real_window_wide = min(windowwidth,windowheight)
                screen.fill((0,0,0))
                screen.blit(pygame.transform.scale(new1surface,(real_window_wide,real_window_wide)),(int((windowwidth-real_window_wide)/2),int((windowheight-real_window_wide)/2)))
                pygame.display.update()
                clock.tick(60)
            player.build_shade()
            ys = []
            for y in range(world_h):
                yt = []
                for i in game_map:
                    for k in range(world_w):
                        if i[y][k]==2:
                            i[y][k]=0
                    yt.append(i[y])
                ys.append(yt)
            for i in ys:
                for x in range(world_w):
                    for y in range(x,world_h):
                        i[x][y],i[y][x] = i[y][x],i[x][y]
                for j in range(world_w):
                    i[j] = i[j][::-1]
            ys2 = []
            for y in range(world_z):
                yt = []
                for i in ys:
                    yt.append(i[y])
                ys2.append(yt)
            #print(ys2)
            for x in range(world_w):
                for y in range(world_w):
                    for z in range(world_w):
                        if type(ys2[z][y][x]) == str:
                            ifaces = ys2[z][y][x]
                            ys2[z][y][x] = ''.join([ifaces[3],ifaces[2],ifaces[0],ifaces[1],ifaces[4],ifaces[5]])
            return ys2   #->game_map
        def turn_2(blockgroup,game_map):#逆时针转动
            drawlist = []#创建画图顺序列表
            playerx,playerz,playery = player.get_world_pos()
            if playerx<0:
                drawlist.append(player)
            for x in range(world_w-1,-1,-1):
                if x==playerx and playery>world_h and not player in drawlist:
                    drawlist.append(player)
                for y in range(world_h):
                    for z in range(world_z):
                        if x==playerx and y==playery:
                            if playerz<0 or z==playerz or (not player in drawlist and z==0):
                                drawlist.append(player)
                        if game_map[z][y][x] == 1 or game_map[z][y][x] == 3 or game_map[z][y][x] == 4 or game_map[z][y][x] == 5 or type(game_map[z][y][x])==str:
                            drawlist.append(blockdict[(x,y,z)])
            if not(player in drawlist):
                drawlist.append(player)
            centerx,centery = basicx+world_lenth*world_w/2,basicy+world_lenth*world_z/2#计算和画图#basicx+world_lenth/2,basicy+world_lenth/2,#(150,150)
            #world_arg
            for block in blockgroup:                                                                            #^z
                block.p1x,block.p1y = block.space_pos[0],block.space_pos[1]                                     #p1—p2
                block.p2x,block.p2y = block.space_pos[0]+world_lenth,block.space_pos[1]                        # |  |
                block.p3x,block.p3y = block.space_pos[0]+world_lenth,block.space_pos[1]+world_lenth           #p4—p3 >x
                block.p4x,block.p4y = block.space_pos[0],block.space_pos[1]+world_lenth                        #
            player.p1x,player.p1y = player.pos[0],player.space_pos[1]
            player.p2x,player.p2y = player.pos[0]+player.l,player.space_pos[1]
            player.p3x,player.p3y = player.pos[0]+player.l,player.space_pos[1]+player.l
            player.p4x,player.p4y = player.pos[0],player.space_pos[1]+player.l
            for arg in range(0,-90,-1):#range(world_arg,world_arg+90,1):#range(90,0,-1):
                pygame.event.get()
                screen.fill((0,0,0))
                for piece in piecegroup:#粒子效果
                    piece.x -= 1
                    if piece.x<0:
                        piece.x = 600
                    pygame.draw.rect(screen,piece.color,(int(piece.x),int(piece.y),piece.l,piece.l))
                for block in drawlist:
                    if block!=player:
                        p1x1 = (block.p1x-centerx)*cos(radians(arg))-(block.p1y-centery)*sin(radians(arg))+centerx
                        p2x1 = (block.p2x-centerx)*cos(radians(arg))-(block.p2y-centery)*sin(radians(arg))+centerx
                        p3x1 = (block.p3x-centerx)*cos(radians(arg))-(block.p3y-centery)*sin(radians(arg))+centerx
                        p4x1 = (block.p4x-centerx)*cos(radians(arg))-(block.p4y-centery)*sin(radians(arg))+centerx
                        if type(block.color) == tuple:
                            pygame.draw.rect(screen,block.color,(p3x1,block.pos[1],p4x1-p1x1,world_lenth))
                        else:
                            if block.type0 == 4:
                                
                                newimg = pygame.transform.scale(block.imgleft,(abs(int(p3x1-p2x1))+1,world_lenth))
                                screen.blit(newimg,(p1x1,block.pos[1]))
                                newimg = pygame.transform.scale(block.img0,(int(p3x1-p4x1),world_lenth))
                                screen.blit(newimg,(p4x1,block.pos[1]))
                            else:
                                newimg = pygame.transform.scale(block.color,(abs(int(p4x1-p1x1))+1,world_lenth))
                                screen.blit(newimg,(p1x1,block.pos[1]))
                                newimg = pygame.transform.scale(block.color,(int(p3x1-p4x1),world_lenth))
                                screen.blit(newimg,(p4x1,block.pos[1]))
                    else:
                        player_p1x1 = (player.p1x-centerx)*cos(radians(arg))-(player.p1y-centery)*sin(radians(arg))+centerx
                        player_p2x1 = (player.p2x-centerx)*cos(radians(arg))-(player.p2y-centery)*sin(radians(arg))+centerx
                        player_p3x1 = (player.p3x-centerx)*cos(radians(arg))-(player.p3y-centery)*sin(radians(arg))+centerx
                        player_p4x1 = (player.p4x-centerx)*cos(radians(arg))-(player.p4y-centery)*sin(radians(arg))+centerx
                        player_p3y1 = (player.p3y-centery)*cos(radians(arg))+(player.p3x-centery)*sin(radians(arg))+centery
                        player.space_pos = [player_p1x1,player_p3y1]
                        player.pos = [player_p1x1,player.pos[1]]
                        newimg = pygame.transform.scale(player.img2,(abs(int(player_p3x1-player_p2x1))+1,int(world_lenth/2)))
                        screen.blit(newimg,(player_p1x1,block.pos[1]))
                        newimg = pygame.transform.scale(player.img2,(int(player_p3x1-player_p4x1),int(world_lenth/2)))
                        screen.blit(newimg,(player_p4x1,block.pos[1]))
                new1surface = screen.subsurface((0, 0, 600, 600)).copy()
                real_window_wide = min(windowwidth,windowheight)
                screen.fill((0,0,0))
                screen.blit(pygame.transform.scale(new1surface,(real_window_wide,real_window_wide)),(int((windowwidth-real_window_wide)/2),int((windowheight-real_window_wide)/2)))
        
                pygame.display.update()
                clock.tick(60)
            player.build_shade()
            ys = []
            for y in range(world_h):
                yt = []
                for i in game_map:
                    for k in range(world_w):
                        if i[y][k]==2:
                            i[y][k]=0
                    yt.append(i[y])
                ys.append(yt)
            for i in ys:
                for x in range(world_w):
                    for y in range(x,world_h):
                        i[x][world_w-1-y],i[y][world_w-1-x] = i[y][world_w-1-x],i[x][world_w-1-y]
                for j in range(world_w):
                    i[j] = i[j][::-1]
            ys2 = []
            for y in range(world_z):
                yt = []
                for i in ys:
                    yt.append(i[y])
                ys2.append(yt)
            for x in range(world_w):
                for y in range(world_w):
                    for z in range(world_w):
                        if type(ys2[z][y][x]) == str:
                            ifaces = ys2[z][y][x]
                            ys2[z][y][x] = ''.join([ifaces[2],ifaces[3],ifaces[1],ifaces[0],ifaces[4],ifaces[5]])
            return ys2   #->game_map
        global black_screen
        def black_screen():
            surface0 = pygame.Surface((800,600))
            surface0.fill((0,0,0,255))
            surface1 = screen.copy()
            a = 250
            for i in range(50):
                pygame.event.get()
                surface0.set_alpha(a)
                a-=5
                screen.blit(surface1,(0,0))
                screen.blit(surface0,(0,0))
                pygame.display.update()
                clock.tick(150)
        def you_win():
            sound2.play()
            if normal_mode:
                global nowlevel
                localstatus = levelsstatus
                localstatus[nowlevel] = 1
                with open(get_path('leveldata.txt'),'w') as f:
                    f.write(str(localstatus))
            win_back2menu.index = 'menu'
            win_replay.index = 're'
            win_continue.index = 'con'
            buttons = [win_back2menu,win_replay,win_continue] if normal_mode else [win_back2menu,win_replay]
            for i in buttons:
                i.update((0,0))
            player.move1Y(0)
            screen.fill((0,0,0))
            for i in piecegroup:
                i.draw()
            player.draw()
            for i in activeblock:
                i.draw()
            background0 = screen.copy()
            screen.fill((0,0,0))
            for i in piecegroup:
                i.draw()
            player.draw()
            for i in activeblock:
                i.draw()
            for i in buttons:
                i.draw(screen)
            screen.blit(win_img,((600-win_img.get_rect().width)//2,10))
            background1 = screen.copy()
            screen.fill((0,0,0))
            screen.blit(win_img,((600-win_img.get_rect().width)//2,10))
            for i in activeblock:
                i.draw()
            background = screen.copy()
            drawpos = (int(player.pos[0]+player.l/2),int(player.pos[1]+player.l/2))
            count = 0
            if drawpos[0]>=300:
                count += 1
            if drawpos[1]>=300:
                count += 2
            if count == 0:
                maxdis = ((drawpos[0]-600)**2+(drawpos[1]-600)**2)**0.5
            elif count == 1:
                maxdis = ((drawpos[0]-0)**2+(drawpos[1]-600)**2)**0.5
            elif count == 2:
                maxdis = ((drawpos[0]-600)**2+(drawpos[1]-0)**2)**0.5
            elif count == 3:
                maxdis = ((drawpos[0]-0)**2+(drawpos[1]-0)**2)**0.5
            for i in range(50):
                pygame.event.get()
                clip_area = pygame.Surface((600,600))
                clip_area.fill((0,0,255))
                clip_area.set_colorkey((255, 255, 0))
                pygame.draw.circle(clip_area, (255, 255, 0),drawpos,int(maxdis*i/50))
                surface1 = background1.copy()
                surface1.blit(clip_area,(0,0))
                surface1.set_colorkey((0,0,255))
                screen.blit(background0,(0,0))
                pygame.draw.circle(screen,(255,255,255),drawpos,int(maxdis*i/50)+3)
                screen.blit(surface1,(0,0))
                new1surface = screen.subsurface((0, 0, 600, 600)).copy()
                real_window_wide = min(windowwidth,windowheight)
                screen.fill((0,0,0))
                screen.blit(pygame.transform.scale(new1surface,(real_window_wide,real_window_wide)),(int((windowwidth-real_window_wide)/2),int((windowheight-real_window_wide)/2)))
                pygame.display.update()
                clock.tick(20)
            player.draw()
            new1surface = screen.subsurface((0, 0, 600, 600)).copy()
            real_window_wide = min(windowwidth,windowheight)
            screen.fill((0,0,0))
            screen.blit(pygame.transform.scale(new1surface,(real_window_wide,real_window_wide)),(int((windowwidth-real_window_wide)/2),int((windowheight-real_window_wide)/2)))
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 2
                    if event.type == pygame.MOUSEMOTION:
                        mousepos = pygame.mouse.get_pos()
                        for button in buttons:
                            button.update((int(mousepos[0]/windowwidth*600),int(mousepos[1]/windowheight*600)))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i in buttons:
                            if i.isclick:
                                sound1.play()
                                if i.index == 'menu':
                                    return 2
                                elif i.index == 're':
                                    return 1
                                elif i.index == 'con':
                                    return 4
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return 1
                        return 2
                screen.blit(background,(0,0))
                for i in piecegroup:
                    i.update()
                    i.draw()
                player.draw()
                for i in buttons:
                    i.draw(screen)
                '''
                ##测试
                mousepos = pygame.mouse.get_pos()
                pygame.draw.circle(screen,(255,0,0),(int(mousepos[0]/windowwidth*300),int(mousepos[1]/windowheight*300)),5)
                ##测试
                '''
                new1surface = screen.subsurface((0, 0, 600, 600)).copy()
                real_window_wide = min(windowwidth,windowheight)
                screen.fill((0,0,0))
                screen.blit(pygame.transform.scale(new1surface,(real_window_wide,real_window_wide)),(int((windowwidth-real_window_wide)/2),int((windowheight-real_window_wide)/2)))
                pygame.display.update()
                clock.tick(20)
        def you_lost():
            screen.fill((0,0,0))
            
            for i in activeblock:
                i.draw()
            screen.blit(lost_img,((600-lost_img.get_rect().width)//2,10))
            background = screen.copy()
            piece = []
            for i in range(4):
                piece.append(Piece1(player.pos))
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return 1
                        if event.key == pygame.K_ESCAPE:
                            return 3
                screen.blit(background,(0,0))
                for i in piece:
                    i.update()
                    i.draw()
                for i in piecegroup:
                    i.update()
                    i.draw()
                new1surface = screen.subsurface((0, 0, 600, 600)).copy()
                real_window_wide = min(windowwidth,windowheight)
                screen.fill((0,0,0))
                screen.blit(pygame.transform.scale(new1surface,(real_window_wide,real_window_wide)),(int((windowwidth-real_window_wide)/2),int((windowheight-real_window_wide)/2)))
                pygame.display.update()
                clock.tick(20)
        screen = pygame.display.set_mode((600,600))#screen = pygame.display.set_mode((800,600),pygame.RESIZABLE)
        pygame.display.set_caption('重组')
        world_upshade = []
        world_downshade = []
        world_leftshade = []
        world_rightshade = []
        blockgroup = []
        blockdict = {}
        world_arg = 0
        #print('level1\n\n\n\n\n',level1)#147a1c34a3b1eBG1f1d154a7
        
        world_h = world_w = world_z = len(level1)#h->y;w->x
        #print(world_h,len(level1))
        basicx = basicy = basicz = (600-len(level1)*world_lenth)/2
        max_y = world_z*world_lenth+basicy*2
        game_map = level1#############
        activeblock,blockgroup,blockdict,blocklist_with_z,player = make_up_map(world_z,world_h,world_w,game_map)
        clock = pygame.time.Clock()
        infoObject = pygame.display.Info()
        windowwidth = infoObject.current_w
        windowheight = infoObject.current_h
        for i in activeblock:
            i.draw()
        player.draw()
        new1surface = screen.subsurface((0, 0, 600, 600)).copy()
        real_window_wide = min(windowwidth,windowheight)
        screen.fill((0,0,0))
        screen.blit(pygame.transform.scale(new1surface,(real_window_wide,real_window_wide)),(int((windowwidth-real_window_wide)/2),int((windowheight-real_window_wide)/2)))
        black_screen()
        reset = False
        piecegroup = []
        for i in range(25):
            pieces = Piece((randint(0,600),randint(-5,600)),piecegroup)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if reset == False:
                            reset = True
                        else:
                            return 1,[screen,clock]
                    else:
                        reset = False
                if event.type == pygame.VIDEORESIZE:
                    infoObject = pygame.display.Info()
                    windowwidth = infoObject.current_w
                    windowheight = infoObject.current_h
                    if windowwidth<300:
                        windowwidth = 300   
                    if windowheight<300:
                        windowheight = 300   
                    screen = pygame.display.set_mode((windowwidth,windowheight),pygame.RESIZABLE)
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_w]:
                player.can_set = False
                player.jump()
            if key_pressed[pygame.K_d]:
                player.can_set = False
                player.moveX(1)
                player.change_dir(1)
            if key_pressed[pygame.K_a]:
                player.can_set = False
                player.moveX(-1)
                player.change_dir(0)
            #if key_pressed[pygame.K_t]:
            #    print(player.can_set)
            if key_pressed[pygame.K_q]:
                #print(player.can_set)
                if player.can_set:
                    player.space_pos = player.lock_pos
                    player.can_set = False
                game_map = turn_1(blockgroup,game_map)#player.moveX(-1)
                world_upshade = []
                world_downshade = []
                world_leftshade = []
                world_rightshade = []
                activeblock,blockgroup,blockdict,blocklist_with_z = make_up_map(world_z,world_h,world_w,game_map)
                world_arg+=90
                player.fall = True
            if key_pressed[pygame.K_e]:
                if player.can_set:
                    player.space_pos = player.lock_pos
                    player.can_set = False
                game_map = turn_2(blockgroup,game_map)#player.moveX(-1)
                world_upshade = []
                world_downshade = []
                world_leftshade = []
                world_rightshade = []
                activeblock,blockgroup,blockdict,blocklist_with_z = make_up_map(world_z,world_h,world_w,game_map)
                world_arg-=90
                player.fall = True
            #if key_pressed[pygame.K_q]:
            #    print(player.get_world_pos())
            if key_pressed[pygame.K_ESCAPE]:
                return 3
            screen.fill((0,0,0))
            for i in piecegroup:
                i.update()
                i.draw()
            for i in activeblock:
                i.draw()
            get_player_return = player.update()
            if get_player_return == 1:#输
                return 1,[screen,clock]
            elif get_player_return == 2:#赢
                return 2
            elif get_player_return == 3:#esc退出
                return 3
            elif get_player_return == 4:#赢并下一关
                return 4
            player.draw()
            new1surface = screen.subsurface((0, 0, 600, 600)).copy()
            real_window_wide = min(windowwidth,windowheight)
            screen.fill((0,0,0))
            screen.blit(pygame.transform.scale(new1surface,(real_window_wide,real_window_wide)),(int((windowwidth-real_window_wide)/2),int((windowheight-real_window_wide)/2)))
            pygame.display.update()
            clock.tick(36)
    def credit():
        back_button.index = 'back'
        showtext1 = Button((int((windowx-464)/2),int(90000/windowy),472,48),buttons.subsurface((0,35,59,6)))
        showtext2 = Button((int((windowx-424)/2),int(180000/windowy),424,48),buttons.subsurface((0,42,53,6)))
        showtext2.index = 'visit'
        buttongroup_credit = [back_button,showtext1,showtext2]
        for i in buttongroup_credit:
            i.update((0,0))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    mousepos = pygame.mouse.get_pos()
                    for button in buttongroup_credit:
                        button.update(mousepos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in buttongroup_credit:
                        if i.isclick:
                            sound1.play()
                            if i.index == 'back':
                                running = False
                            elif i.index == 'visit':
                                webbrowser.open('https://space.bilibili.com/482077400')
            screen.fill((0,0,0))
            for i in piecegroup:
                i.update()
                i.draw(screen)
            for i in buttongroup_credit:
                i.draw(screen)
            pygame.display.update()
            clock.tick(60)
    class Slider():
        def __init__(self,pos,lenth=200,height=10,value=0.5,backcolor=(0,255,0),buttoncolor=(255,255,255)):
            self.drag = False
            self.pos = pos
            self.w = lenth
            self.h = height
            self.color = backcolor
            button_img = pygame.Surface((height,height))
            button_img.fill(buttoncolor)
            self.button = Button((int(self.pos[0]+lenth*value),self.pos[1],height,height),button_img)
            self.value = value
        def update(self,mousepos,click):
            self.button.update(mousepos)
            if self.button.isclick:
                if click==1:
                    self.drag = True
                elif click==0:
                    self.drag = False
            else:
                self.drag = False
            if self.drag:
                if self.pos[0]<mousepos[0]<self.pos[0]+self.w:
                    self.button.move((int(mousepos[0]-self.h/2),self.button.pos[1]))
                    self.value = round((self.button.pos[0]+self.h/2-self.pos[0])/self.w,2)
        def draw(self,screen):
            pygame.draw.rect(screen,self.color,(self.pos[0],self.pos[1],self.w,self.h))
            self.button.draw(screen)
    def setting():
        global music_setting
        with open(get_path('setting.txt'),'r') as f:
            music_setting = eval(f.read())
        back_button.index = 'back'
        slider1 = Slider((int(windowx*0.3),int(windowy*0.3)),value=music_setting[0],lenth=300,height=20,backcolor=(0,0,255))
        slider2 = Slider((int(windowx*0.3),int(windowy*0.6)),value=music_setting[1],lenth=300,height=20)
        showtext1 = Button((int(windowx*0.1),int(windowy*0.3),145,30),buttons.subsurface((30,21,29,6)))
        showtext2 = Button((int(windowx*0.1),int(windowy*0.6),145,30),buttons.subsurface((30,28,29,6)))
        clearbutton = Button((int(windowx*0.1),int(windowy*0.9),290,30),buttons.subsurface((0,49,59,6)))
        clearbutton.index = 'clear'
        running = True
        buttongroup_setting = [back_button,showtext1,showtext2,clearbutton]
        for i in buttongroup_setting:
            i.update((0,0))
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    mousepos = pygame.mouse.get_pos()
                    slider1.update(mousepos,None)
                    slider2.update(mousepos,None)
                    for button in buttongroup_setting:
                        button.update(mousepos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    slider1.update(mousepos,1)
                    slider2.update(mousepos,1)
                    for i in buttongroup_setting:
                        if i.isclick:
                            sound1.play()
                            if i.index == 'back':
                                running = False
                                with open(get_path('setting.txt'),'w') as f:
                                    f.write(str(music_setting))
                            if i.index == 'clear':
                                sure_clear = True
                                enterbox1 = Enterbox((0,200,500,30),text='Click here and type "I am sure" to continue.')
                                global enterbox_get_clear
                                enterbox_get_clear = True
                                while sure_clear:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()
                                        if event.type == pygame.MOUSEMOTION:
                                            mousepos = pygame.mouse.get_pos()
                                            back_button.update(mousepos)
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            if enterbox1.update0(pygame.mouse.get_pos()) == 2:
                                                enterbox_get_clear = False
                                            if back_button.isclick:
                                                sure_clear = False
                                        if event.type == pygame.KEYDOWN:
                                            if enterbox1.active:
                                                enterbox1.update1(event)
                                    screen.fill((0,0,0))
                                    for i in piecegroup:
                                        i.update()
                                        i.draw(screen)
                                    back_button.draw(screen)
                                    enterbox1.draw(screen)
                                    if enterbox1.text == 'I am sure':
                                        with open(get_path('leveldata.txt'),'w') as f:
                                            f.write('[0,0,0,0,0,0,0,0,0,0]')##############正式版改成60个0#################################################################
                                        sure_clear = False
                                        for i in buttongroup_setting:
                                            i.update((0,0))
                                    pygame.display.update()
                                    clock.tick(60)
                                for i in buttongroup_setting:
                                    i.update((0,0))
                if event.type == pygame.MOUSEBUTTONUP:
                    mousepos = pygame.mouse.get_pos()
                    slider1.update(mousepos,0)
                    slider2.update(mousepos,0)
                    #print(slider1.value,slider2.value)
                    music_setting = [slider1.value,slider2.value]
                    for sound in sounds:
                        sound.set_volume(slider2.value)
            screen.fill((0,0,0))
            for i in piecegroup:
                i.update()
                i.draw(screen)
            for i in buttongroup_setting:
                i.draw(screen)
            slider1.draw(screen)
            slider2.draw(screen)
            pygame.display.update()
            clock.tick(60)

    class Enterbox():
        def __init__(self,rect,active_color=(0,255,0),inactive_color=(255,0,0),text=''):
            self.rect = pygame.Rect(rect)
            self.w0 = self.rect[2]
            self.w = self.w0
            self.h = self.rect[3]
            self.pos = [rect[0],rect[1]]
            self.color_inactive = inactive_color
            self.color_active = active_color
            self.color = inactive_color
            self.active = False
            self.text = text
        def update0(self,mousepos):
            global enterbox_get_clear
            if self.pos[0] <= mousepos[0] <= self.pos[0]+self.rect[2] and self.pos[1] <= mousepos[1] <= self.pos[1]+self.rect[3]:
                sound1.play()
                self.active = True
                self.color = self.color_active
                if enterbox_get_clear:
                    self.text = ''
                    return 2
            else:
                self.active = False
                self.color = self.color_inactive
        def update1(self,event):
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            if event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                self.text = paste()
        def draw(self,screen):
            txt_surface = font.render(self.text, True, self.color)
            self.w = max(self.w0, txt_surface.get_width() + 10)
            self.pos[0] = (windowx-self.w)//2
            if self.pos[0]<0:
                self.pos[0] = 0
            screen.blit(txt_surface, (self.pos[0] + 5, self.pos[1] + 5))
            pygame.draw.rect(screen, self.color, (self.pos[0],self.pos[1],self.w,self.h), 2)
            
    def load_level():
        global enterbox_get_clear,screen
        back_button.index = 'back'
        load_button = Button((280,350,240,60),buttons.subsurface((0,28,24,6)))
        load_button.index = 'ok'
        enterbox = Enterbox((0,200,500,30),text='Click here and enter the code or press ctrl+v to paste the code.')
        buttongroup_load_level = [back_button,load_button]
        for i in buttongroup_load_level:
            i.update((0,0))
        in_load_level = True
        enterbox_get_clear = True
        
        while in_load_level:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    mousepos = pygame.mouse.get_pos()
                    for button in buttongroup_load_level:
                        button.update(mousepos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if enterbox.update0(pygame.mouse.get_pos()) == 2:
                        enterbox_get_clear = False
                    for i in buttongroup_load_level:
                        if i.isclick:
                            sound1.play()
                            if i.index == 'back':
                                in_load_level = False
                            elif i.index == 'ok':
                                try:
                                    clevel = decode2(enterbox.text)
                                    is_win = False
                                    #print(clevel)
                                    while True:
                                        clevel = decode2(enterbox.text)
                                        re = main(clevel,False)
                                        if re == 2 or re == 3:
                                            break
                                except:
                                    enterbox.text = 'Not a correct code'
                                    enterbox_get_clear = True
                                if not pygame.get_init():
                                    pygame.quit()
                                    exit()
                                screen = pygame.display.set_mode((800,600))
                if event.type == pygame.KEYDOWN:
                    if enterbox.active:
                        enterbox.update1(event)
            screen.fill((0,0,0))
            for i in piecegroup:
                i.update()
                i.draw(screen)
            for i in buttongroup_load_level:
                i.draw(screen)
            enterbox.draw(screen)
            pygame.display.update()
            clock.tick(60)
        
    def choose_level():
        global screen
        def generate_points(w, h, l, m):
            # 预计算总宽度和总高度
            total_width = 5 * l + 4 * m
            total_height = 2 * l + m
            # 计算起始偏移量
            dx = (w - total_width) / 2
            dy = (h - total_height) / 2
            # 计算每个正方形之间的步长
            step = l + m
            # 生成点坐标
            points = []
            for i in range(2):  # 两行
                for j in range(5):  # 五列
                    x = dx + j * step
                    y = dy + i * step
                    points.append((x, y))
            return points
        page = 0
        back_button.index = 'back'
        nextpage = Button((int(windowx*0.1),int(windowy*0.9),45,30),buttons.subsurface((30,1,9,6)))
        lastpage = Button((int(windowx*0.8),int(windowy*0.9),45,30),buttons.subsurface((39,1,9,6)))
        nextpage.index = 'last'
        lastpage.index = 'next'
        buttongroup_choose_level = [back_button,nextpage,lastpage]
        for i in buttongroup_choose_level:
            i.update((0,0))
        for i in buttongroup_choose_level:
            i.isclick = False
        pointslist = generate_points(windowx,windowy,50,30)
        level_button = [[],[],[],[],[],[]]
        for i in range(1,11):##############正式版更换为右侧####for i in range(1,61):########################################################################
            newsurface = pygame.Surface((20,20))
            newsurface.fill((255, 152, 0) if levelsstatus[i-1] else (255, 232, 36))
            text = font.render(str(i),True,(255,255,255))
            newsurface.blit(text,(0,0))
            #print((i-1)//10)
            newbutton = Button((pointslist[(i-1)%10][0],pointslist[(i-1)%10][1],50,50),newsurface)
            newbutton.index = int(i)
            level_button[(i-1)//10].append(newbutton)
            
        activebutton = level_button[0]

        in_choose_level = True
        while in_choose_level:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    mousepos = pygame.mouse.get_pos()
                    for button in buttongroup_choose_level:
                        button.update(mousepos)
                    for button in activebutton:
                        button.update(mousepos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in buttongroup_choose_level:
                        if i.isclick:
                            sound1.play()
                            if i.index == 'back':
                                in_choose_level = False
                            elif i.index == 'next':
                                if page < maxpage-1:
                                    page += 1
                                    activebutton = level_button[page]
                            elif i.index == 'last':
                                if page > 0:
                                    page -= 1
                                    activebutton = level_button[page]
                    for i in activebutton:
                        if i.isclick:
                            sound1.play()
                            is_win = False#干啥的?
                            levelcounter = 0#用于进入下一关
                            global nowlevel
                            while True:
                                nowlevel = i.index-1+levelcounter
                                clevel = decode2(levels[i.index-1+levelcounter])
                                re = main(clevel)
                                if re == 2 or re==3:
                                    #重新生成关卡按钮以刷新状态
                                    level_button = [[],[],[],[],[],[]]
                                    for i in range(1,11):##############正式版更换为右侧####for i in range(1,61):########################################################################
                                        newsurface = pygame.Surface((20,20))
                                        newsurface.fill((255, 152, 0) if levelsstatus[i-1] else (255, 232, 36))
                                        text = font.render(str(i),True,(255,255,255))
                                        newsurface.blit(text,(0,0))
                                        #print((i-1)//10)
                                        newbutton = Button((pointslist[(i-1)%10][0],pointslist[(i-1)%10][1],50,50),newsurface)
                                        newbutton.index = int(i)
                                        level_button[(i-1)//10].append(newbutton)
                                    activebutton = level_button[0]
                                    break
                                elif re == 4:
                                    levelcounter += 1
                                    if i.index+levelcounter>len(levels):
                                        #重新生成关卡按钮以刷新状态
                                        level_button = [[],[],[],[],[],[]]
                                        for i in range(1,11):##############正式版更换为右侧####for i in range(1,61):########################################################################
                                            newsurface = pygame.Surface((20,20))
                                            newsurface.fill((255, 152, 0) if levelsstatus[i-1] else (255, 232, 36))
                                            text = font.render(str(i),True,(255,255,255))
                                            newsurface.blit(text,(0,0))
                                            #print((i-1)//10)
                                            newbutton = Button((pointslist[(i-1)%10][0],pointslist[(i-1)%10][1],50,50),newsurface)
                                            newbutton.index = int(i)
                                            level_button[(i-1)//10].append(newbutton)
                                        activebutton = level_button[0]
                                        break
                            #print(i.index)
                            screen = pygame.display.set_mode((800,600))
            screen.fill((0,0,0))
            for i in piecegroup:
                i.update()
                i.draw(screen)
            for i in buttongroup_choose_level:
                i.draw(screen)
            for i in activebutton:
                i.draw(screen)
            pygame.display.update()
            clock.tick(60)
    global screen
    global music_setting
    windowx = 800
    windowy = 600
    music_setting = [0.5,0.5]
    pygame.init()
    screen = pygame.display.set_mode((windowx,windowy))
    pygame.display.set_caption('重组')
    title = pygame.image.load(get_path('title.png'))
    title_rect = title.get_rect()
    title = pygame.transform.scale(title,(int(title_rect[2]*10),int(title_rect[3]*10)))
    title.set_colorkey((0,0,0))
    back = pygame.image.load(get_path('title.png'))
    buttons = pygame.image.load(get_path('caidan.png'))
    start_button = Button((320,270,290,60),buttons.subsurface((0,0,29,6)))
    load_button = Button((320,350,240,60),buttons.subsurface((0,28,24,6)))
    setting_button = Button((320,430,410,60),buttons.subsurface((0,7,41,6)))
    credits_button = Button((320,510,410,60),buttons.subsurface((0,14,41,6)))
    
    back_button = Button((20,20,240,60),buttons.subsurface((0,21,24,6)))
    buttongroup = [start_button,setting_button,credits_button,load_button]
    font = pygame.font.Font(None,30)
    pygame.display.update()
    clock = pygame.time.Clock()
    piecegroup = []
    for i in range(25):
        piecegroup.append(Piece((randint(1,799),randint(-599,599)),piecegroup))

    maxpage = 6     #选关界面，最大页数

    #win界面，ui
    _dx = 30
    _wid = 53
    win_back2menu = Button((150*_k-_wid*_k*1.5-_dx,210*_k,_wid*_k,_wid*_k),buttons.subsurface((42,7,7,7)))
    win_replay = Button((150*_k-_wid*_k*0.5,210*_k,_wid*_k,_wid*_k),buttons.subsurface((50,7,7,7)))
    win_continue = Button((150*_k+_wid*_k*0.5+_dx,210*_k,_wid*_k,_wid*_k),buttons.subsurface((42,13,7,7)))
        
    #################################加载本体
    world_lenth = 35
    icon = pygame.image.load(get_path('myicon.png'))
    pygame.display.set_icon(icon)
    end_img = pygame.image.load(get_path('end.png'))#结束文字
    #print(end_img.get_rect())
    ele_img = pygame.image.load(get_path('eles1.png'))#方块素材图片
    win_img = end_img.subsurface([0,0,36,6])
    win_img.set_colorkey((0,0,0))
    win_rect = win_img.get_rect()
    win_img = pygame.transform.scale(win_img,(5*win_rect[2]*_k,5*win_rect[3]*_k))
    lost_img = end_img.subsurface([0,7,35,6])
    lost_img.set_colorkey((0,0,0))
    lost_rect = lost_img.get_rect()
    lost_img = pygame.transform.scale(lost_img,(5*lost_rect[2]*_k,5*lost_rect[3]*_k))
    block1_img = ele_img.subsurface([0,0,10,10])#基础块
    block1_img = pygame.transform.scale(block1_img,(world_lenth,world_lenth))
    block2_img = ele_img.subsurface([10,0,10,10])#锚点
    block2_img = pygame.transform.scale(block2_img,(world_lenth,world_lenth))
    block3_img = ele_img.subsurface([20,0,10,10])#终点
    block3_img = pygame.transform.scale(block3_img,(world_lenth,world_lenth))
    block4_img = ele_img.subsurface([50,20,10,10])#寄块
    block4_img = pygame.transform.scale(block4_img,(world_lenth,world_lenth))
    player1_img = ele_img.subsurface([30,30,10,10])#玩家(睁眼)
    player1_img = pygame.transform.scale(player1_img,(int(world_lenth/2),int(world_lenth/2)))
    player2_img = ele_img.subsurface([40,30,10,10])#玩家(闭眼)
    player2_img = pygame.transform.scale(player2_img,(int(world_lenth/2),int(world_lenth/2)))
    channel_imgs = {}
    loadpos = ((30,0),(40,0),(50,0),(0,10),(10,10),(20,10),(30,10),(40,10),(50,10),(0,20),(10,20),(20,20),(30,20),(40,20),(10,30),(20,30),(0,20))
    facescode = ('0000','1000','0100','0010','0001','1100','0110','0011','1001','1101','1110','0111','1011','1111','0101','1010','1')#上左下右
    for i in range(17):
        #print(loadpos[i])
        channel_imgs[facescode[i]] = pygame.transform.scale(ele_img.subsurface(loadpos[i][0],loadpos[i][1],10,10),(world_lenth,world_lenth))# = ele_img.subsurface([50,20,60,30])
    '''
    block1_img = ele_img.subsurface([0,0,20,20])#基础块
    block1_img = pygame.transform.smoothscale(block1_img,(world_lenth,world_lenth))
    block2_img = ele_img.subsurface([20,0,20,20])#锚点
    block2_img = pygame.transform.scale(block2_img,(world_lenth,world_lenth))
    block3_img = ele_img.subsurface([40,0,20,20])#终点
    block3_img = pygame.transform.scale(block3_img,(world_lenth,world_lenth))
    block4_img = ele_img.subsurface([100,40,20,20])#寄块
    block4_img = pygame.transform.scale(block4_img,(world_lenth,world_lenth))
    player1_img = ele_img.subsurface([60,60,20,20])#玩家(睁眼)
    player1_img = pygame.transform.scale(player1_img,(int(world_lenth/2),int(world_lenth/2)))
    player2_img = ele_img.subsurface([80,60,20,20])#玩家(闭眼)
    player2_img = pygame.transform.scale(player2_img,(int(world_lenth/2),int(world_lenth/2)))
    channel_imgs = {}
    loadpos = ((60,0),(80,0),(100,0),(0,20),(20,20),(40,20),(60,20),(80,20),(100,20),(0,40),(20,40),(40,40),(60,40),(80,40),(20,60),(40,60),(0,60))
    facescode = ('0000','1000','0100','0010','0001','1100','0110','0011','1001','1101','1110','0111','1011','1111','0101','1010','1')#上左下右
    for i in range(17):
        channel_imgs[facescode[i]] = pygame.transform.scale(ele_img.subsurface(loadpos[i][0],loadpos[i][1],20,20),(world_lenth,world_lenth))# = ele_img.subsurface([50,20,60,30])
    '''
    #################################加载本体

    #################################音频初始化
    sound0 = pygame.mixer.Sound(get_path('jump.mp3'))
    sound1 = pygame.mixer.Sound(get_path('tap.mp3'))
    sound2 = pygame.mixer.Sound(get_path('get3.mp3'))
    sounds = [sound0,sound1,sound2]
    
    with open(get_path('setting.txt'),'r') as f:
        music_setting = eval(f.read())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
                for button in buttongroup:
                    button.update(mousepos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isclick:
                    sound1.play()
                    levels = None
                    levelsstatus = None
                    with open(get_path('level.txt'),'r') as file:
                        try:
                            levels = eval(file.read().replace('\n',''))
                        except:
                            print('关卡数据错误或丢失')
                    with open(get_path('leveldata.txt'),'r') as file:
                        try:
                            levelsstatus = eval(file.read())
                        except:
                            print('关卡数据错误或丢失')
                    if not((levels is None)or(levelsstatus is None)):
                        choose_level()
                elif setting_button.isclick:
                    sound1.play()
                    setting()
                elif credits_button.isclick:
                    sound1.play()
                    credit()
                elif load_button.isclick:
                    sound1.play()
                    load_level()
                for i in buttongroup:
                    i.update((0,0))
        screen.fill((0,0,0))
        screen.blit(title,(20,20))
        #screen.blit(background,(0,0))
        for i in piecegroup:
            i.update()
            i.draw(screen)
        for i in buttongroup:
            i.draw(screen)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    dict1 = {'000000': 'AA', '000001': 'AB', '000010': 'AC', '000011': 'AD',
             '000100': 'AE', '000101': 'AF', '000110': 'AG', '000111': 'AH',
             '001000': 'AI', '001001': 'AJ', '001010': 'AK', '001011': 'AL',
             '001100': 'AM', '001101': 'AN', '001110': 'AO', '001111': 'AP',
             '010000': 'AQ', '010001': 'AR', '010010': 'AS', '010011': 'AT',
             '010100': 'AU', '010101': 'AV', '010110': 'AW', '010111': 'AX',
             '011000': 'AY', '011001': 'AZ', '011010': 'BA', '011011': 'BB',
             '011100': 'BC', '011101': 'BD', '011110': 'BE', '011111': 'BF',
             '100000': 'BG', '100001': 'BH', '100010': 'BI', '100011': 'BJ',
             '100100': 'BK', '100101': 'BL', '100110': 'BM', '100111': 'BN',
             '101000': 'BO', '101001': 'BP', '101010': 'BQ', '101011': 'BR',
             '101100': 'BS', '101101': 'BT', '101110': 'BU', '101111': 'BV',
             '110000': 'BW', '110001': 'BX', '110010': 'BY', '110011': 'BZ',
             '110100': 'CA', '110101': 'CB', '110110': 'CC', '110111': 'CD',
             '111000': 'CE', '111001': 'CF', '111010': 'CG', '111011': 'CH',
             '111100': 'CI', '111101': 'CJ', '111110': 'CK', '111111': 'CL'}
    dict2 = {'AA': '000000', 'AB': '000001', 'AC': '000010', 'AD': '000011',
             'AE': '000100', 'AF': '000101', 'AG': '000110', 'AH': '000111',
             'AI': '001000', 'AJ': '001001', 'AK': '001010', 'AL': '001011',
             'AM': '001100', 'AN': '001101', 'AO': '001110', 'AP': '001111',
             'AQ': '010000', 'AR': '010001', 'AS': '010010', 'AT': '010011',
             'AU': '010100', 'AV': '010101', 'AW': '010110', 'AX': '010111',
             'AY': '011000', 'AZ': '011001', 'BA': '011010', 'BB': '011011',
             'BC': '011100', 'BD': '011101', 'BE': '011110', 'BF': '011111',
             'BG': '100000', 'BH': '100001', 'BI': '100010', 'BJ': '100011',
             'BK': '100100', 'BL': '100101', 'BM': '100110', 'BN': '100111',
             'BO': '101000', 'BP': '101001', 'BQ': '101010', 'BR': '101011',
             'BS': '101100', 'BT': '101101', 'BU': '101110', 'BV': '101111',
             'BW': '110000', 'BX': '110001', 'BY': '110010', 'BZ': '110011',
             'CA': '110100', 'CB': '110101', 'CC': '110110', 'CD': '110111',
             'CE': '111000', 'CF': '111001', 'CG': '111010', 'CH': '111011',
             'CI': '111100', 'CJ': '111101', 'CK': '111110', 'CL': '111111'}

    main0()
