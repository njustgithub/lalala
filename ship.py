import pygame

from game_functions import ship_hit

from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.image = pygame.image.load('images/xiao.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.image_height = self.image.get_height()
        self.image_width = self.image.get_width()
        # print(self.image_height,self.image_width )

        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.bottom)

        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False

    def update_location(self):
        if self.moving_right:
            self.center_x += self.ai_settings.ship_speed_factor
            if self.center_x >= self.screen_rect.right - self.image_width/2:
                self.center_x = self.screen_rect.right-self.image_width/2

        if self.moving_left:
            self.center_x -= self.ai_settings.ship_speed_factor
            if self.center_x <= self.image_width/2:
                self.center_x = self.image_width/2

        if self.moving_down:
            self.center_y += self.ai_settings.ship_speed_factor
            if self.center_y >= self.screen_rect.bottom:
                self.center_y = self.screen_rect.bottom
        # print(self.center_y, self.rect.bottom)
        if self.moving_up:
            self.center_y -= self.ai_settings.ship_speed_factor
            if self.center_y <= self.image_height:
                    self.center_y = self.image_height

        self.rect.centerx = self.center_x
        self.rect.bottom = self.center_y

    def blitme(self):

        self.screen.blit(self.image, self.rect)
        # print(self.rect.centerx)

    def center_ship(self):
        self.center_x = self.screen_rect.centerx
        self.center_y = self.screen_rect.bottom
        # print(self.center, self.screen_rect.centerx)

    def check_aliens_bottom(self, ai_settings, stats, screen, ship, aliens, bullets):
        screen_rect = screen.get_rect()
        for alien in aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
                break


