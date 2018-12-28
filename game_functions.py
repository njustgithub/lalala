import sys

from time import sleep
import pygame

from bullet import Bullet

from alien import Alien


#按键事件触发
def check_keydown_event(event, ai_settings, screen, ship, bullets, stats):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_SPACE:
        if ai_settings.consequent_enable:
            ai_settings.bullet_consequent = True
        else:
            fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_F1:
        if not stats.game_active:
            stats.enter_flag = True
        # print(stats.enter_flag)


def check_keyup_event(event, ship, ai_settings):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_SPACE:
        ai_settings.bullet_consequent = False


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets, stats)
            if stats.enter_flag:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets,
                              mouse_x, mouse_y,sb)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship, ai_settings)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets,
                      mouse_x, mouse_y, sb)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets,
                      mouse_x, mouse_y, sb):
    if (not stats.game_active and play_button.rect.collidepoint(mouse_x, mouse_y)) or stats.enter_flag:
        # print('llllllll')
        stats.game_active = True
        stats.reset_stats()

        sb.prep_ships()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_score()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        pygame.mouse.set_visible(False)

        ai_settings.initialize_dynamic_settings()
        stats.enter_flag = False


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship, sb, stats):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.top <= 0:
            bullets.remove(bullet)
    check_bullet_alien_colllide(ai_settings, screen, ship, aliens, bullets, sb, stats)


#子弹和外星人的碰撞检测   外星人被消灭完后重新生成一组
def check_bullet_alien_colllide(ai_settings, screen, ship, aliens, bullets, sb, stats):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)#碰撞检测
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        stats.level += 1
        sb.prep_level()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ai_settings.increase_speed()


def fire_bullet(ai_settings, screen, ship, bullets):
    # print(ai_settings.bullet_consequent)
        if ai_settings.bullet_consequent:
            ai_settings.num += 1
            if ai_settings.num > 30:
                new_bullet = Bullet(ai_settings, screen, ship)
                bullets.add(new_bullet)
                ai_settings.num = 0
        else:
            if len(bullets) < ai_settings.bullets_allowed:
                new_bullet = Bullet(ai_settings, screen, ship)
                bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,  alien.rect.height)
    for alien_number in range(number_aliens_x):
        for row in range(number_rows):
            create_alien(ai_settings, screen, aliens, alien_number, row)

#每行的外星人数


def get_number_aliens(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2.2 * alien_width))
    return number_aliens_x


#多少行外星人

def get_number_rows(ai_settings, ship_height,  alien_height):
    available_space_y = ai_settings.screen_height - 5 * alien_height -ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, number_rows):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.x
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = float(alien.x)
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * number_rows
    aliens.add(alien)


#碰撞相应
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    # print(stats.ship_limit)
    if stats.ship_left <= 1:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    else:
        stats.ship_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(1)


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    ship.check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
        print('shit')


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


