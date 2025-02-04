from random import randint
from src.config.variables import win_width, win_height, lost
from src.sprites.game_sprite import GameSprite

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1