import pygame
import os
from random import randint

# Конфигурация
from src.config.variables import *
from src.config.constants import FPS

# Спрайты
from src.sprites.player import Player
from src.sprites.enemy import Enemy
from src.sprites.asteroid import Asteroid

# Эффекты
from src.effects.explosion import EnemyExplosion, AsteroidExplosion
from src.effects.scrolling_background import ScrollBackground

# Утилиты
from src.utils.asset_loader import AssetLoader

# Инициализация pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
pygame.init()
pygame.mixer.init()

# Загрузка звуков
pygame.mixer.music.load(AssetLoader.get_asset_path('sounds', 'space.ogg'))
pygame.mixer.music.play(-1)
fire_sound = AssetLoader.load_sound('fire.ogg')
explosion_sound = AssetLoader.load_sound('explosion.mp3')
vzriv_sound = AssetLoader.load_sound('vzriv.ogg')

font1 = pygame.font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = pygame.font.Font(None, 36)

pygame.display.set_caption('Shooter')
mw = pygame.display.set_mode((win_width, win_height))
bg = pygame.transform.scale(pygame.image.load(img_back), (win_width, win_height))

# Создаем объект фона со скроллингом
background = ScrollBackground(img_back)

# В разделе инициализации игры
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
enemies = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()  # Это уже есть, оставляем
explosions = pygame.sprite.Group()  # Новая группа для взрывов

def add_enemy():
    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    enemies.add(enemy)

def add_asteroid():
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 60, 60, 1)
    asteroids.add(asteroid)

for i in range(1, 6):
    add_enemy()

for i in range(1, 3):
    add_asteroid()

finish = False
run = True

# Игровой цикл
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_sound.play()
                bullets = ship.fire()

    if not finish:
        # Обновляем и отрисовываем скроллинг фона
        background.update()
        background.draw(mw)        
        
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        mw.blit(text, (10, 20))
        
        # Обновление спрайтов
        ship.update()
        enemies.update()
        asteroids.update()
        bullets.update()
        explosions.update()  # Обновляем взрывы
        
        # Отрисовка спрайтов
        ship.reset(mw)
        enemies.draw(mw)
        asteroids.draw(mw)
        bullets.draw(mw)
        explosions.draw(mw)  # Отрисовываем взрывы

        # Проверка столкновений
        collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for collision in collisions:
            explosion1 = EnemyExplosion(collision.rect.centerx, collision.rect.centery)
            explosions.add(explosion1)
            explosion_sound.play()
            score += 1
            add_enemy()

        asteroid_hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in asteroid_hits:
            explosion2 = AsteroidExplosion(hit.rect.centerx, hit.rect.centery)
            explosions.add(explosion2)
            vzriv_sound.play()
            add_asteroid()        

        if score >= 10:
            mw.blit(win, (win_width//2-100, win_height//2-50))
            finish = True
        elif lost >= max_lost:
            mw.blit(lose, (win_width//2-100, win_height//2-50))
            finish = True

    pygame.display.update()
    pygame.time.delay(1000 // FPS)

pygame.quit()