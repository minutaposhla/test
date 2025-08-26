#Создай собственный Шутер!

from pygame import *
from random import randint, randrange
from time import sleep

window = display.set_mode((700,500))

display.set_caption("Шутер")

clock = time.Clock()

game = True

font.init()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed, size):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.speed = sprite_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        self.rect.x -= self.speed if keys_pressed[K_LEFT] and self.rect.x > 5 else 0
        self.rect.x += self.speed if keys_pressed[K_RIGHT] and self.rect.x < 695 else 0

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx - 8, self.rect.top, 10, 20)
        bullet.add(bullets)

    

class Enemy(GameSprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed, size, hp, min_sp, max_sp, often_sp):
        super().__init__(sprite_image, sprite_x, sprite_y, sprite_speed, size)
        self.hp = hp
        self.appearance_time = randrange(min_sp, max_sp, often_sp)
        self.move = False
    
    def appearance(self, min_sp, max_sp, often_sp):
        self.appearance_time -= 1

        if self.appearance_time == 0 and self.move == False:
            self.appearance_time = randrange(min_sp, max_sp, often_sp)
            self.rect.x = randint(5, 630)
            self.move = True
    
    def update(self):
        if self.move == True:
            if self.rect.y < 500:
                self.rect.y += self.speed
            else:
                self.rect.y = -65
                self.move = False
                self.appearance_time = randrange(48, 120, 1)
                bg.count -= 1
            # self.rect.y += self.speed if self.rect.y < 500 else self.rect.y -= 566
        # if self.rect.y < 500:
        #     self.rect.y += self.speed

class Bullet(GameSprite): 
    def update(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            self.kill()

class Background(sprite.Sprite):
    def __init__(self, bg_list):
        super().__init__()
        self.count = 0
        self.bg_list = bg_list

    
    def update(self):
        if self.count < -5:
            self.count = -5
        if self.count > 5:
            self.count = 5

        self.background = transform.scale(image.load(self.bg_list[self.count + 5]), (700,500))




enemies = sprite.Group()
bullets = sprite.Group()

ufo1 = Enemy("ufo.png", 1, -65, 2, 65, 3, 48, 120, 1)
ufo2 = Enemy("ufo.png", 1, -65, 3, 65, 3, 48, 120, 1)
ufo3 = Enemy("ufo.png", 1, -65, 4, 65, 3, 48, 120, 1)
asteroid1 = Enemy("asteroid.png", 1, -80, 2, 80, 4, 120, 240, 1)
asteroid2 = Enemy("asteroid.png", 1, -80, 1, 80, 4, 120, 240, 1)

ufo1.add(enemies)
ufo2.add(enemies)
ufo3.add(enemies)
asteroid1.add(enemies)
asteroid2.add(enemies)

player = Player("rocket.png", 320, 430, 10, 65)

bg = Background(["galaxy — -5.jpg","galaxy — -4.jpg","galaxy — -3.jpg","galaxy — -2.jpg","galaxy — -1.jpg",
"galaxy.jpg","galaxy — 1.jpg","galaxy — 2.jpg","galaxy — 3.jpg","galaxy — 4.jpg", "galaxy — 5.jpg"])

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_UP:
                player.fire()

    bg.update()
    window.blit(bg.background, (0,0))

    player.reset()
    player.update()

    enemies.update()
    enemies.draw(window)

    bullets.update()
    bullets.draw(window)

    ufo1.appearance(48, 120, 1)
    ufo2.appearance(48, 120, 1)
    ufo3.appearance(48, 120, 1)
    asteroid1.appearance(120, 240, 1)
    asteroid2.appearance(120, 240, 1)

    sprite_list = sprite.groupcollide(
        enemies, bullets, False, True
    )

    for enemy in sprite_list:
        if enemy.hp == 4:
            pass
        else:
            enemy.hp -= 1
            if enemy.hp == 0:
                enemy.rect.y = -65
                enemy.hp = 3
                enemy.move = False
                enemy.rect.x = randint(5, 630)
                enemy.appearance_time = randrange(48, 120, 1)
                
                sound_effect = mixer.Sound("fire.ogg")
                sound_effect.play()

                bg.count += 1

    sprite_list = sprite.spritecollide(
        player, enemies, True
    )

    for enemy in sprite_list:
        bg.count -= 4

    if bg.count == -5:
        bg.update()
        window.blit(bg.background, (0,0))
        display.update()
        sleep(3)
        break

    if bg.count == 5:
        bg.update()
        window.blit(bg.background, (0,0))
        display.update()
        sleep(3)
        break

    clock.tick(24)

    display.update()