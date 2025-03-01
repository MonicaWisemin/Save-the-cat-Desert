import random
import pygame
import cat as cat_m
from ghost import Ghost as ghost_m
from agent import choose_action, get_state_index,get_state, Q_TABLE
import math
import Buttons
import numpy as np


#setting a window
pygame.init()

screen_width = 1280
screen_height = 720


#in game pics
screen = pygame.display.set_mode((screen_width,screen_height))      #display the window
pygame.display.set_caption('Save the cat!Desert')
background = pygame.image.load('E:\\pythonProject2\\pics\\staay\\map.png').convert_alpha()
background = pygame.transform.scale(background,(1280,720))
bg_height = background.get_height()

#start menu
start_bg = pygame.image.load('E:\\pythonProject2\\pics\\menu\\start_main.png')
resized_stbg = pygame.transform.scale(start_bg, (1280, 720))
stitle = pygame.image.load('E:\\pythonProject2\\pics\\menu\\title.png')
start_menu = pygame.image.load('E:\\pythonProject2\\pics\\menu\\start_menu.png')
resized_stitle = pygame.transform.scale(stitle, (730, 130))
re_stmenu = pygame.transform.scale(start_menu, (560, 420))

#buttons on the start menu
startB = pygame.image.load('E:\\pythonProject2\\pics\\menu\\start.png').convert_alpha()
quitB = pygame.image.load('E:\\pythonProject2\\pics\\menu\\quit.png').convert_alpha()
collectionB = pygame.image.load('E:\\pythonProject2\\pics\\menu\\collection.png').convert_alpha()
re_stB = pygame.transform.scale(startB, (230, 90))
re_qB = pygame.transform.scale(quitB, (230, 90))
re_colB = pygame.transform.scale(collectionB, (450, 90))
pauseB = pygame.image.load('E:\\pythonProject2\\pics\\menu\\buttons\\pause_button.png')
re_pauseB = pygame.transform.scale(pauseB,(70,70))


#collection page
collectionBG = pygame.image.load('E:\\pythonProject2\\pics\\staay\\map_desert.png')
collectionG = pygame.image.load('E:\\pythonProject2\\pics\\staay\\collec\\collectionP.png')
re_colBG = pygame.transform.scale(collectionBG, (1280, 720))
re_colG = pygame.transform.scale(collectionG,(1250,526))

collectionT = pygame.image.load('E:\\pythonProject2\\pics\\staay\\collec\\collectionT.png')
re_colT = pygame.transform.scale(collectionT,(996, 210))

backB = pygame.image.load('E:\\pythonProject2\\pics\\menu\\pause menu\\back.png').convert_alpha()
re_bkB = pygame.transform.scale(backB,(150,90))

#add font
font = pygame.font.SysFont('Arial',35)
font1 = pygame.font.SysFont('Arial',25)


start_game = False

scroll1 = 0
tilesBG = math.ceil(screen_height / bg_height) + 1


clock = pygame.time.Clock()
FPS = 60

start_game = False
main_menu = False
collection_Page = False

#setup for player movement
mov_left = False
mov_right = False
shoot = False

#load agent we trained
try:
    Q_TABLE = np.load("q_table.npy")
    print("Q-Table loaded successfully.")
except FileNotFoundError:
    print("Q-Table not found. Please train the agent first using agent.py.")
    Q_TABLE = None


#load images
#bullet
bullet_img = pygame.image.load('E:\\pythonProject2\\pics\\item\\bullet.png').convert_alpha()
#coin
coin_img = pygame.image.load('E:\\pythonProject2\\pics\\item\\coin.png').convert_alpha()

#state images
coin_s_img = pygame.image.load('E:\\pythonProject2\\pics\\menu\\state\\coin_s.png').convert_alpha()
catSave_t_img = pygame.image.load('E:\\pythonProject2\\pics\\menu\\state\\cat_save_time.png').convert_alpha()
re_cs = pygame.transform.scale(coin_s_img,(90,35))
re_cst = pygame.transform.scale(catSave_t_img,(150,35))



#set the player class
class player(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.shoot_cooldown = 0
        ##add animation to the in-game player
        self.animation_list = []
        self.index = 0
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.direction = -1
        self.coin = 0
        self.ghostKilled = 0


        for i in range(3):
            image = pygame.image.load(f'E:\\pythonProject2\\pics\\move\\player\\{i}.png')
            image = pygame.transform.scale(image,(100,100))
            self.animation_list.append(image)
        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def move(self,moving_left,moving_right):
        #reset movement variables
        dx = 0
        dy = 0

        #assign movement
        if moving_left:
            dx = -self.speed
        if moving_right:
            dx = self.speed

         #movement update
        self.rect.x += dx
        self.rect.y += dy
        # player boundaries control
        if self.rect.x <= 300:
            self.rect.x = 300
        elif self.rect.x >= 600:
            self.rect.x = 600

    def shoot(self):
        bullet = Bullet(self.rect.centerx - 50, self.rect.centery, self.direction)
        bullet_group.add(bullet)


    def update_animation(self):
        #timer
        ani_cooldown = 100
        #update image
        self.image = self.animation_list[self.frame_index]
        #check if enough time passed since the last update
        if pygame.time.get_ticks() - self.update_time > ani_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #run out animation
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0




    def draw(self):
        screen.blit(self.image, self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        #check bullet collide
        if pygame.sprite.spritecollide(self,ghost_group,True):
            self.kill()
            playeri.ghostKilled +=1


class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(coin_img,(30,30))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x,y)
        self.speed = 10

    def update(self) :
        #coin move with screen
        self.rect.y -= self.speed
        if self.rect.y <= 50:
            self.kill()
        #check player get coins
        if pygame.sprite.collide_rect(self,playeri):
            playeri.coin += 1
        #delete coin
            self.kill()

def rentex():
    global  Ctext_sur,Gtext_rect,Gtext_sur,Gtext_rect
    Ctext_sur = font.render(f'{playeri.coin}', True, (255, 255, 255))
    Ctext_rect = Ctext_sur.get_rect()
    Gtext_sur = font.render(f'{playeri.ghostKilled}', True, (255, 255, 255))
    Gtext_rect = Gtext_sur.get_rect()


def reset_T():
    bullet_group.empty()
    ghost_group.empty()
    coin_group.empty()

startButton = Buttons.Buttons(780, 370, re_stB)
quitButton = Buttons.Buttons(780, 470, re_qB)
collectionButton = Buttons.Buttons(760, 570, re_colB)
pauseButton = Buttons.Buttons(1200,10,re_pauseB)

#create sprite gruops
bullet_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

#temp coin
#coin = coin(350,50)
#coin_group.add(coin)

#create player instance
playeri = player(600,50,5)
#create cat instance
cati = cat_m.cat(240,640,5)
#randomly create ghost instance
next_ghost_time = pygame.time.get_ticks() + random.randint(2000,5000)
#randomly create coins
next_coin = pygame.time.get_ticks() +random.randint(3000,7000)

#speed = 1
run = True
while run:
    #avoid the trail of player left behind, aka refreshment
    clock.tick(FPS)


    game_totalT = 30*1000
    game_totalT -= 1000
    start_timeT = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()

        #display the backgroud and scroll it
    for i in range(0,tilesBG):
        screen.blit(background,(0,i * bg_height + scroll1))
        scroll1 -= 5
        #scroll check
    if abs(scroll1) > bg_height:
        scroll1 = 0
    #create the pause menu
    if pauseButton.draw(screen):
        pass
    rentex()

    screen.blit(re_cs,(10,10))
    screen.blit(re_cst, (10,45))
    screen.blit(Ctext_sur,(105,10))
    screen.blit(Gtext_sur,(165,45))

    key_status = []
    if mov_left:
        key_status.append(font1.render("Left key pressed", True, (255, 255, 255)))
    if mov_right:
        key_status.append(font1.render("Right key pressed", True, (255, 255, 255)))
    if shoot:
        key_status.append(font1.render("Space key pressed", True, (255, 255, 255)))

    for i, status in enumerate(key_status):
        screen.blit(status, (10, 80 + i * 30))

    #check if cat is disappeared
    if not cati.isalive:
        print('Game over')



    #spawn ghost randomly
    if not ghost_group and current_time >= next_ghost_time:
        x = 240
        y = 50
        speed = 10
        ghost = ghost_m(x,y,speed)
        ghost_group.add(ghost)
        next_ghost_time = current_time + random.randint(2000,5000)

        if ghost.state == 1:
            start_game = False


    if not coin_group and current_time >= next_coin:
        x = random.randint(320,580)
        y = 640
        coin = Coin(x,y)
        coin_group.add(coin)
        next_coin = current_time + random.randint(3000,7000)


    playeri.update_animation()
    playeri.draw()

        #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)


    cati.update_animation()
    cati.draw(screen)

    coin_group.draw(screen)
    coin_group.update()

    playeri.move(mov_left,mov_right)
    ghost_group.update(bullet_group,cati)
    ghost_group.draw(screen)

    if shoot:
        playeri.shoot()
            #for bullet in bullet_group:
                #print(f"Bullet rect: x={bullet.rect.x}, y={bullet.rect.y}")



        # check if ghost catches cat
    cati.check_cap(ghost_group)

    if cati.state == 1:
        print('The final ghost kill number is :', playeri.ghostKilled)
        print('The final coins get number is :', playeri.coin)
        reset_T()
        playeri.ghostKilled = 0
        playeri.coin = 0
        start_game = False

    if game_totalT <=0:
        endT = pygame.time.get_ticks()
        runT = endT - start_timeT
        print('total run time:',runT)
        cati.state = 1
    state = get_state(playeri.rect.x, cati.rect.x, cati.rect.y,
                      coin_group.sprites()[0].rect.x if coin_group else 0,
                      coin_group.sprites()[0].rect.y if coin_group else 0)
    state_index = get_state_index(state)
    if Q_TABLE is not None:
        action = choose_action(state_index)
    else:
        action = random.choice([0,1,2])

    # actions
    if action == 0:
        mov_left = True
        mov_right = False
    elif action == 1:
        mov_right = True
        mov_left = False
    elif action == 2:
        shoot = True

    pygame.display.update()

    #close the game when hit the x button on the right-up side of the window
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            run = False

        #keyboard press
        if event.type == pygame.KEYDOWN:
            '''
            if event.key == pygame.K_LEFT:
                mov_left = True
                #Ltext_sur = font1.render("left key pressed", True, (255, 255, 255))
                #screen.blit(Ltext_sur, (10, 80))

            if event.key == pygame.K_RIGHT:
                mov_right =True
                #Rtext_sur = font1.render("right key pressed", True, (255, 255, 255))
                #screen.blit(Rtext_sur, (10, 80))
            if event.key == pygame.K_SPACE:
                shoot = True
                #Stext_sur = font1.render("Space key pressed", True, (255, 255, 255))
                #screen.blit(Stext_sur, (10, 115))
            '''
            if event.key == pygame.K_ESCAPE:
                start_game = False

        #keyboard release
        if event.type == pygame.KEYUP:
            pass
            '''
            if event.key == pygame.K_LEFT:
                mov_left = False
            if event.key == pygame.K_RIGHT:
                mov_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            '''




pygame.quit()