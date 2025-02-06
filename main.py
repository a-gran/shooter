# Импортируем необходимые библиотеки
import pygame               # Основная библиотека для создания игр
import os                   # Для работы с путями к файлам
from random import randint  # Для генерации случайных чисел

# Импортируем все переменные из файла конфигурации
from src.config.variables import *
from src.config.constants import FPS

# Импортируем классы спрайтов
from src.sprites.player import Player
from src.sprites.enemy import Enemy
from src.sprites.asteroid import Asteroid

# Импортируем эффекты
from src.effects.explosion import EnemyExplosion, AsteroidExplosion
from src.effects.scrolling_background import ScrollBackground

# Импортируем утилиты и обработку коллизий
from src.utils.asset_loader import AssetLoader
from src.effects.collisions import *

# Скрываем приветственное сообщение pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
pygame.init()
pygame.mixer.init()

# Загружаем звуки
pygame.mixer.music.load(AssetLoader.get_asset_path('sounds', 'space.ogg'))
pygame.mixer.music.play(-1)
fire_sound = AssetLoader.load_sound('fire.ogg')
explosion_sound = AssetLoader.load_sound('explosion.mp3')
vzriv_sound = AssetLoader.load_sound('vzriv.ogg')

# Создаем шрифты и текст
font1 = pygame.font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = pygame.font.Font(None, 36)

# Настраиваем окно игры
pygame.display.set_caption('Shooter')
mw = pygame.display.set_mode((win_width, win_height))
background = ScrollBackground(img_back)

# Создаем игрока и группы спрайтов
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
enemies = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Функция добавления врага
def add_enemy():
    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    enemies.add(enemy)

# Функция добавления астероида
def add_asteroid():
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 60, 60, 1)
    asteroids.add(asteroid)

# Создаем начальных врагов и астероидов
for i in range(1, 6):
    add_enemy()
for i in range(1, 3):
    add_asteroid()

# Инициализация игровых флагов
finish = False
run = True

# Основной игровой цикл
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            fire_sound.play()
            bullets = ship.fire()

    if not finish:
        # Обновляем и отрисовываем игровые объекты
        background.update()
        background.draw(mw)
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        mw.blit(text, (10, 20))
        
        # Обновляем все спрайты
        for sprite in [ship, enemies, asteroids, bullets, explosions]:
            sprite.update()

        # Отрисовываем все спрайты
        ship.reset(mw)
        for sprite in [enemies, asteroids, bullets, explosions]:
            sprite.draw(mw)

        # Обрабатываем коллизии
        hits = check_bullet_enemy_collisions(enemies, bullets, explosions, explosion_sound)
        score += hits
        
        if score >= 10:
            show_victory_animation(background, mw, ship, enemies, asteroids, explosions)
            handle_victory(mw, win, win_width, win_height, ship, enemies, bullets, asteroids)
            finish = True
        elif hits > 0:
            add_enemy()
        
        if handle_bullet_asteroid_collisions(asteroids, bullets, explosions, vzriv_sound):
            add_asteroid()
        
        if handle_player_collisions(ship, enemies, asteroids, explosions, 
                                  explosion_sound, background, mw, lose, 
                                  win_width, win_height):
            finish = True

    pygame.display.update()
    pygame.time.delay(1000 // FPS)

pygame.quit()