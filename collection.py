import sys
import pygame
import Buttons
import start_menuing


pygame.init()

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width,screen_height))      #display the window
pygame.display.set_caption('Save the cat! Desert')
background = pygame.image.load('E:\\pythonProject2\\pics\\staay\\map_desert.png')
resized_bg = pygame.transform.scale(background,(1280,720))

#import the title surface
title = pygame.image.load('E:\\pythonProject2\\pics\\staay\\collec\\collectionT.png')
collect_menu = pygame.image.load('E:\\pythonProject2\\pics\\staay\\collec\\collectionP.png')
scale1 = 0.8
scale2 = 0.6
resized_title = pygame.transform.scale(title,(996, 210))
re_colmenu = pygame.transform.scale(collect_menu,(1250,526))

#import the game start buttons
backB = pygame.image.load('E:\\pythonProject2\\pics\\menu\\pause menu\\back.png').convert_alpha()

re_bkB = pygame.transform.scale(backB,(150,90))



#creat button class

#create button instances
backButton =   Buttons.Buttons(10,10,re_bkB)


run = True
while run:
#display the title and the start menu
    screen.blit(resized_bg,(0,0))
    #screen.blit(resized_title,(142,5))
    screen.blit(re_colmenu,(10,150))
    screen.blit(resized_title,(142,5))
    #display the buttons
    if backButton.draw(screen) :
        start_menuing.run = True
        print('back to the start menu!')
        sys.exit()



         #press d and player move to its right
    pygame.display.update()
#close the game when hit the x button on the right-up side of the window
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            run = False

pygame.quit()