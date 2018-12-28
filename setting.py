import pygame
class Settings():


    def __init__(self):
        #游戏界面设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.3
        #子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        self.bullet_consequent = False
        self.consequent_enable = True  #连发使能标志位
        self.num = 0
        #外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1    #1向右 -1向左
        self.alien_points = 50
        #飞船设置
        self.ship_limit = 3
        # 外星人移动速度增加
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        #分值比例
        self.score_scale = 1.5

        # self.bgm = pygame.mixer.music.load("music/bgm.wav")


    def initialize_dynamic_settings(self):
        self.alien_speed_factor = 1.5
        self.ship_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_points = 50
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.score_scale * self.alien_points)
        # print(self.alien_points)
