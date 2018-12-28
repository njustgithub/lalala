import game_functions as gf
import pygame

from ship import Ship
from button import Button
from game_stats import GameStats

from alien import Alien

from scoreboard import Scoreboard

from setting import Settings


from pygame.sprite import Group


def run_game():

    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    sb = Scoreboard(ai_settings, screen, stats)
    # alien = Alien(ai_settings, screen)
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # bgm = ai_settings.bgm
    # pygame.mixer.music.load("music/sheji.ogg")
    # pygame.mixer.music.play(-1, 0.0)
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)
        if stats.game_active:
            if ai_settings.bullet_consequent:  #连发控制
                gf.fire_bullet(ai_settings, screen, ship, bullets)
            ship.update_location()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship, sb, stats)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb)
# print(ai_settings.bullet_consequent)

run_game()
