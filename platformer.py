import pygame
import pickle
from os import path
from pygame.locals import *
from pygame import mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1,0.0,5000)
coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.5)
pygame.init()
screen_width=1000
screen_height=1000
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("superplatformer100proznevirus")
tile_size=50
cf=pygame.image.load("img/sky.png")
cb=pygame.image.load("img/restart_btn.png")
cstart=pygame.image.load("img/start_btn.png")
cexit=pygame.image.load("img/exit_btn.png")
menu=True
gameover=0
level=1
makslevel=7
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)
score=0
white=(255,255,255)
black=(0,0,0)

def draw_text(text,font,text_col,x,y):
    image=font.render(text,True,text_col)
    screen.blit(image,(x,y))

def reset_level(level):
    player.reset(100 , screen_height - 130)
    enemy_group.empty()
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()
    platform_group.empty()

    if path.exists(f"level{level}_data"):
        pickle_in = open(f"level{level}_data","rb")
        world_data = pickle.load(pickle_in)
    score_coin=Coin(20,18)
    coin_group.add(score_coin)
    world = World(world_data)

    return world

def draw_grid():
    for i in range(0,20):
        pygame.draw.line(screen,(0,0,0),(0,i*tile_size),(screen_width,i*tile_size))
        pygame.draw.line(screen,(0,0,0),(i*tile_size,0),(i*tile_size,screen_height))

class World():
    def __init__(self,data):
        self.tile_list=[]
        dirtimg=pygame.image.load("img/dirt.png")
        grassimg=pygame.image.load("img/grass.png")
        rowcount=0
        for row in data:
            colcount=0
            for tile in row:
                if tile==1:
                    img=pygame.transform.scale(dirtimg,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=colcount*tile_size
                    img_rect.y=rowcount*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)

                if tile==2:
                    img=pygame.transform.scale(grassimg,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=colcount*tile_size
                    img_rect.y=rowcount*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)

                if tile==3:
                    enemy=Enemy(colcount*tile_size,rowcount*tile_size+15)
                    enemy_group.add(enemy)

                if tile==4:
                    lava=Lava(colcount*tile_size,rowcount*tile_size+(tile_size//2))
                    lava_group.add(lava)

                if  tile==5:
                    exit=Exit(colcount*tile_size,rowcount*tile_size+(tile_size//2))
                    exit_group.add(exit)

                if  tile==6:
                    coin=Coin(colcount*tile_size+(tile_size//2),rowcount*tile_size+(tile_size//2))
                    coin_group.add(coin)

                if  tile==7:
                    platform=Platform(colcount*tile_size,rowcount*tile_size,1,0)
                    platform_group.add(platform)

                if  tile==8:
                    platform=Platform(colcount*tile_size,rowcount*tile_size,0,1)
                    platform_group.add(platform)

                colcount+=1
            rowcount+=1

                

    def draw(self):
        for i in self.tile_list:
            screen.blit(i[0],i[1])

class player():
    def __init__(self,x,y):
        self.reset(x,y)



    def update(self,gameover):
        dx=0
        dy=0
        walkcd=5
        if gameover == 0:
            key=pygame.key.get_pressed()
            if key [pygame.K_SPACE]and self.jumped==False and self.inair==False:
                jump_fx.play()
                self.vel_y =-17
                self.jumped=True

            if key [pygame.K_SPACE]==False:
                self.jumped=False

            if key [pygame.K_a]:
                dx-=4
                self.counter+=1
                self.direction=-1

            if key[pygame.K_d]:
                dx+=4
                self.counter+=1
                self.direction=1
            if key[pygame.K_a ]==False and key[pygame.K_d]==False:
                self.counter=0
                self.index=0
                if self.direction==1:
                    self.image=self.images_right[self.index]
                if self.direction==-1:
                    self.image=self.images_left[self.index]

            if self.counter>walkcd:
                self.counter=0
                self.index+=1
                if self.index>=len(self.images_right):
                    self.index=0
                if self.direction==1:
                    self.image=self.images_right[self.index]
                if self.direction==-1:
                    self.image=self.images_left[self.index]

            self.vel_y+=1
            if self.vel_y>10:
                self.vel_y=10
            dy+=self.vel_y
            self.inair=True


            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y,self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom 
                        self.vel_y = 0
                        self.inair=False
            
            if pygame.sprite.spritecollide(self,enemy_group,False):
                gameover=-1
                game_over_fx.play()
            if pygame.sprite.spritecollide(self,lava_group,False):
                gameover=-1
                game_over_fx.play()
            if pygame.sprite.spritecollide(self,exit_group,False):
                gameover=1
            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y,self.width, self.height):
                    dx=0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if abs((self.rect.top+dy)-platform.rect.bottom)<20:
                        self.vel_y=0
                        dy=platform.rect.bottom-self.rect.top
                    elif abs((self.rect.bottom+dy)-platform.rect.top)<20:
                        self.rect.bottom=platform.rect.top-1
                        self.inair=False
                        dy=0
                    if platform.move_x!=0:
                        self.rect.x+=platform.move_direction

            self.rect.x+=dx
            self.rect.y+=dy
        
        elif gameover == -1:
            self.image = self.dead_image
            if self.rect.y >200:
                self.rect.y-=5
        # if self.rect.bottom>screen_height:
        #     self.rect.bottom=screen_height
        #     dy=0
        screen.blit(self.image,self.rect)
        return gameover
    def reset(self,x,y):
        self.inair=True
        img=pygame.image.load("img/guy1.png")
        self.image= pygame.transform.scale(img,(40,80))
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y= 0
        self.direction=0
        self.jumped= False
        self.images_right=[]
        self.images_left=[]
        self.index=0
        self.counter=0
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.dead_image = pygame.image.load("img/ghost.png")
        for i in range(1,5):
            img_right=pygame.image.load(f"img/guy{i}.png")
            img_right=pygame.transform.scale(img_right,(40,80))
            img_left=pygame.transform.flip(img_right,True,False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/blob.png")
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.md=1
        self.mc=0
    def update(self):
        self.rect.x+=self.md
        self.mc+=1
        if abs(self.mc)>50:
            self.mc*=-1
            self.md*=-1

class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        image=pygame.image.load("img/lava.png")
        self.image=pygame.transform.scale(image,(tile_size,tile_size//2))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y


class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        image=pygame.image.load("img/exit.png")
        self.image=pygame.transform.scale(image,(tile_size,int(tile_size*1.5)))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y



class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.clicked=False
    def draw(self):
        result=False
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                result=True
                self.clicked=True
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False
        screen.blit(self.image,self.rect)
        return result
    

class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        image=pygame.image.load("img/coin.png")
        self.image=pygame.transform.scale(image,(tile_size//2,tile_size//2))
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y


    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

world_data=[
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 2, 2, 2, 0, 2, 0, 2, 0, 2, 0, 0, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 4, 4, 2, 2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 3, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]   
player=player(100,850)
enemy_group=pygame.sprite.Group()
lava_group=pygame.sprite.Group()
exit_group=pygame.sprite.Group()
score_coin=Coin(20,18)
coin_group=pygame.sprite.Group()
coin_group.add(score_coin)
platform_group=pygame.sprite.Group()
if path.exists(f"level{level}_data"):
    pickle_in=open(f"level{level}_data","rb")
    world_data=pickle.load(pickle_in)
world=World(world_data)
restartbtn=Button(screen_width//2,screen_height//2,cb)
startbtn=Button(screen_width//2-350,screen_height//2,cstart)
exitbtn=Button(screen_width//2+150,screen_height//2,cexit)
run=True
while run:
    screen.blit(cf,(0,0))
    if menu==True:
        if exitbtn.draw():
            run=False
        if startbtn.draw():
            menu=False
    else:
        world.draw()
        if gameover == 0:
            enemy_group.update()
            platform_group.update()
            if pygame.sprite.spritecollide(player,coin_group,True):
                score+=1
                coin_fx.play()
            draw_text(str(score),font_score,white,tile_size-10,10)
            



        enemy_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        coin_group.draw(screen)
        gameover = player.update(gameover)
        if gameover==-1:
            if restartbtn.draw():
                world_data=[]
                world=reset_level(level)
                gameover=0
                score=0
        if gameover==1:
            level+=1
            if level<=makslevel:
                world_data=[]
                world=reset_level(level)
                gameover=0
            else:
                if restartbtn.draw():
                    level=1
                    world_data=[]
                    world=reset_level(level)
                    gameover=0


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    pygame.display.update()

pygame.quit()