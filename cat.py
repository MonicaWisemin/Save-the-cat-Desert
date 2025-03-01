import pygame
import ghost

pygame.init()

clock = pygame.time.get_ticks()
FPS = 60
speed = 5

class cat(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.animation_list = []
        self.start_time = 0
        self.index = 0
        self.state = 0 #0:normal; 1:caught
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.isalive = True
        temp_list = []
        for i in range(3):
            cat = pygame.image.load(f'E:\\pythonProject2\\pics\\move\\cat\\{i}.png')
            cat = pygame.transform.scale(cat,(80,80))
            temp_list.append(cat)
        self.animation_list.append(temp_list)

        temp_list = []
        for i in range(3):
            cat = pygame.image.load(f'E:\\pythonProject2\\pics\\move\\capcat\\{i}.png')
            cat = pygame.transform.scale(cat,(80,80))
            temp_list.append(cat)
        self.animation_list.append(temp_list)

        self.cat = self.animation_list[self.action][self.frame_index]
        self.rect = self.cat.get_rect()
        self.rect.center = (x,y)

    def update_animation(self):
        # timer
        ani_cooldown = 100
        # update image
        self.cat = self.animation_list[self.action][self.frame_index]
        # check if enough time passed since the last update
        if pygame.time.get_ticks() - self.update_time > ani_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #check if run out animation
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update(self, new_action):
        #check if new action is different to previous action
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_cap(self, ghost_group):
        # 遍历 ghost_group 中的每个 Ghost 实例
        for ghost in ghost_group:
            col_ghost = pygame.sprite.spritecollide(self,ghost_group,False)
            if col_ghost:  # 检查 Ghost 的 rect 是否与 Cat 的 rect 发生碰撞
                #if self.state == 0:  # 如果 Cat 当前状态是正常
                self.state = 1  # 设置 Cat 的状态为“被抓”
                self.update(1)  # 更新状态为“被抓”
                self.start_time = pygame.time.get_ticks()

                break  # 一旦检测到碰撞，退出循环
            else:
                # 如果没有检测到碰撞，重置状态
                self.state = 0
                self.update(0)

        if self.state == 1:
            elasp_time = pygame.time.get_ticks() - self.start_time
            print(self.state)
            if elasp_time >= 1000:
                self.state = 2
                self.isalive = False
                print('Cat being caped')

    def draw(self,surface):
        if self.state != 2:
            surface.blit(self.cat,self.rect)
