import pygame.ftfont


from pygame.sprite import Group

from ship import Ship


class Scoreboard():

    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    # 当前分数
    def prep_score(self):
        # score_stc = str(self.stats.score)
        rounded_score = int(round(self.stats.score, -1))
        score_stc = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_stc, True,
                        self.text_color, self.ai_settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    # 最高分
    def prep_high_score(self):
        # 图像
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                        self.text_color, self.ai_settings.bg_color)
        # 位置
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.top = 0
        self.high_score_rect.centerx = self.screen_rect.centerx

    # 当前等级
    def prep_level(self):
        self.level_str = str(self.stats.level)
        self.level_image = self.font.render(self.level_str, True,
                        self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom
        self.level_rect.centerx = self.score_rect.centerx

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = ship_number * ship.rect.width
            ship.rect.y = 0
            self.ships.add(ship)


    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)





