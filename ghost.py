import pygame
import random


pygame.init()

clock = pygame.time.get_ticks()
FPS = 60
speed = 10



class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.moving = False
        self.start_time = pygame.time.get_ticks()
        #self.start_time = 0
        self.animation_list = []
        self.index = 0
        self.frame_index = 0
        self.isalive = True
        self.update_time = pygame.time.get_ticks()
        self.state = 0  # 0: normal; 1: caught cat and stay; 2: disappear
        for i in range(3):
            image = pygame.image.load(f'E:\\pythonProject2\\pics\\move\\ghost\\{i}.png')
            image = pygame.transform.scale(image, (80, 80))
            self.animation_list.append(image)
        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        # timer
        ani_cooldown = 100
        # update image
        self.image = self.animation_list[self.frame_index]
        # check if enough time passed since the last update
        if pygame.time.get_ticks() - self.update_time > ani_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # check if run out animation
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def chase_cat(self, cat):
        if self.state == 0:
            elasp_time = pygame.time.get_ticks() - self.start_time
            self.moving = True
            if self.moving:
                 if elasp_time >= 3 * 1000:
                    if self.rect.centery < cat.rect.centery- 10:
                        self.rect.centery += self.speed
                    if self.rect.colliderect(cat.rect):
                        self.state = 1
                        self.start_time = pygame.time.get_ticks()
        elif self.state == 1:
            elasp_time = pygame.time.get_ticks() - self.start_time
            if elasp_time >= 3000:
                self.state = 2


    def draw(self, surface):
        if self.state != 2:
            surface.blit(self.ghost, self.rect)



    def update(self, bullet_group, cat):
        # 更新动画
        self.update_animation()

        # 检测子弹碰撞
        if pygame.sprite.spritecollide(self,bullet_group,True):
            self.kill()


        # 根据状态更新行为
        if self.state == 0:
            # 正常移动逻辑
            self.chase_cat(cat)
        elif self.state == 1:
            # 被抓住后停留 3 秒
            stop_time = pygame.time.get_ticks() - self.start_time
            if stop_time >= 3000:  # 停留 3 秒后消失
                self.state = 2
        elif self.state == 2:
            # 消失逻辑
            self.kill()  # 从精灵组中移除