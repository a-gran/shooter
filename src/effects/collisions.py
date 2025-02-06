# src/game/collisions.py
import pygame
from src.effects.explosion import EnemyExplosion, AsteroidExplosion

def handle_bullet_enemy_collision(collision, explosions, explosion_sound):
    """Обработка одного столкновения пули с врагом"""
    explosion = EnemyExplosion(collision.rect.centerx, collision.rect.centery)
    explosions.add(explosion)
    explosion_sound.play()

def check_bullet_enemy_collisions(enemies, bullets, explosions, explosion_sound):
    """Проверка столкновений пуль с врагами"""
    collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for collision in collisions:
        handle_bullet_enemy_collision(collision, explosions, explosion_sound)
    return len(collisions)

def handle_bullet_asteroid_collisions(asteroids, bullets, explosions, vzriv_sound):
    """Проверка столкновений пуль с астероидами"""
    collisions = pygame.sprite.groupcollide(asteroids, bullets, True, True)
    for collision in collisions:
        explosion = AsteroidExplosion(collision.rect.centerx, collision.rect.centery)
        explosions.add(explosion)
        vzriv_sound.play()
    return len(collisions) > 0

def handle_player_collisions(player, enemies, asteroids, explosions, explosion_sound, background, mw, lose_text, win_width, win_height):
    """Обработка столкновений игрока"""
    if pygame.sprite.spritecollide(player, enemies, True) or pygame.sprite.spritecollide(player, asteroids, True):
        explosion = EnemyExplosion(player.rect.centerx, player.rect.centery)
        explosions.add(explosion)
        explosion_sound.play()
        
        while len(explosions) > 0:
            background.update()
            background.draw(mw)
            explosions.update()
            explosions.draw(mw)
            pygame.display.update()
            pygame.time.delay(20)
            
        mw.blit(lose_text, (win_width//2-100, win_height//2-50))
        pygame.display.update()
        return True
    return False

def show_victory_animation(background, mw, ship, enemies, asteroids, explosions):
    """Отображение анимации взрыва при победе"""
    while len(explosions) > 0:
        background.update()
        background.draw(mw)
        ship.reset(mw)
        enemies.draw(mw)
        asteroids.draw(mw)
        explosions.update()
        explosions.draw(mw)
        pygame.display.update()
        pygame.time.delay(20)

def handle_victory(mw, win_text, win_width, win_height, ship, enemies, bullets, asteroids):
    """Обработка победы игрока"""
    mw.blit(win_text, (win_width//2-100, win_height//2-50))
    pygame.display.update()
    pygame.time.delay(2000)
    
    ship.kill()
    enemies.empty()
    bullets.empty()
    asteroids.empty()