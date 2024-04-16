import pygame
from pygame.locals import *
from random import randint
from time import time as timer # импортируем функцию для засекания времени, чтобы интерпретатор не искал эту функцию в pygame модуле time, даем ей другое название сами
# подгружаем отдельно функции для работы со шрифтом

pygame.font.init()
font1 = pygame.font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = pygame.font.Font(None, 36)

#фоновая музыка
pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()
fire_sound = pygame.mixer.Sound('fire.ogg')

# нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_bullet = "bullet.png" # пуля
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_ast = "asteroid.png" # астероид

score = 0 # сбито кораблей
goal = 20 # столько кораблей нужно сбить для победы
lost = 0 # пропущено кораблей
max_lost = 10 # проиграли, если пропустили столько
life = 3  # очки жизни

# класс-родитель для других спрайтов
class GameSprite(pygame.sprite.Sprite):
 # конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       # Вызываем конструктор класса (Sprite):
       pygame.sprite.Sprite.__init__(self)

       # каждый спрайт должен хранить свойство image - изображение
       self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
       self.speed = player_speed

       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 # метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

# класс спрайта-пули
class Bullet(GameSprite):
   # движение врага
   def update(self):
       self.rect.y += self.speed
       # исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()

# класс главного игрока
class Player(GameSprite):
   # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# класс спрайта-врага
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, fluct):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        # Вызываем конструктор класса (Sprite):
        self.fluct = fluct
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        direction = randint(1,2)
        # исчезает, если дойдет до края экрана
        if direction == 1:
            self.rect.x += self.fluct
        elif direction == 2:
            self.rect.x -= self.fluct
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

# Создаем окошко
win_width = 1000
win_height = 700
pygame.display.set_caption("Shooter")
window = pygame.display.set_mode((win_width, win_height))
background = pygame.transform.scale(pygame.image.load(img_back), (win_width, win_height))
# создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# создание группы спрайтов-врагов
monsters = pygame.sprite.Group()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5), randint(40, 50))
    monsters.add(monster)

# создание группы спрайтов-астероидов ()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7), 0)
    asteroids.add(asteroid)

# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна
rel_time = False # флаг отвечающий за перезарядку
num_fire = 0  # переменная для подсчта выстрела

while run:
    # событие нажатия на кнопку Закрыть
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                # проверяем сколько выстеров сделано и не происходит ли перезарядка
                if num_fire < 10 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()

                if num_fire  >= 5 and rel_time == False : # если игрок сделал 5 выстрелов
                    last_time = timer() # засекаем время, когда это произошло
                    rel_time = True # ставив флаг перезарядки

    # сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        # обновляем фон
        window.blit(background,(0,0))
        # производим движения спрайтов
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        # перезарядка
        if rel_time == True:
            now_time = timer() # считываем время

            if now_time - last_time < 2: # пока не прошло 3 секунды выводим информацию о перезарядке
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0   # обнуляем счетчик пуль
                rel_time = False # сбрасываем флаг перезарядки

        # проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = pygame.sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # этот цикл повторится столько раз, сколько монстров подбито
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5), randint(40, 50))
            monsters.add(monster)

        # возможный проигрыш: пропустили слишком много или герой столкнулся с врагом или астероидом
        '''if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) or lost >= max_lost:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))'''

        # если спрайт коснулся врага уменьшает жизнь
        if pygame.sprite.spritecollide(ship, monsters, False) or pygame.sprite.spritecollide(ship, asteroids, False):
            pygame.sprite.spritecollide(ship, monsters, True)
            pygame.sprite.spritecollide(ship, asteroids, True)
            life -= 1
        #проигрыш
        if life == 0 or lost >= max_lost:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))
        # проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        # пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # задаем разный цвет в зависимости от кол-ва жизней
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        pygame.display.update()

    #бонус: автоматический перезапуск игры
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        pygame.time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5), randint(40, 50))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7), 0)
            asteroids.add(asteroid)

    pygame.time.delay(50)
