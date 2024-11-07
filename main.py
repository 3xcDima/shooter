from pygame import *
from time import time as t
mixer.init()
from random import *

window_height = 500
window_weight = 700
window = display.set_mode((window_weight, window_height))
display.set_caption("Shooter game")
background= transform.scale(image.load("galaxy.jpg"), (window_weight, window_height))
mixer.music.load("space.ogg")

clock = time.Clock()
FPS = 40

mixer.music.play()
amount_lives = 3
lost = 0
kills = 0
num_fire = 0
timer = 0
rel_time = False
font.init()
font1 = font.Font(None, 30)
font2 = font.Font(None, 75)




class GameSprite(sprite.Sprite):
    def __init__(self, player_speed, player_x, player_y, player_image):
        super().__init__()
        self.player_speed = player_speed
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < window_weight-65:
            self.rect.x += 10
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 10
    def fire(self):
        bullet = Bullet(5, self.rect.x, self.rect.top-65,'bullet.png')
        print(self.rect.y, self.rect.top)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        if self.rect.y < window_height:
            self.rect.y -= self.player_speed
        else:
            self.kill()
bullets = sprite.Group()
class Enemy(GameSprite):


    def update(self):
        if self.rect.y < window_height:
            self.rect.y += self.player_speed

        else:
            global lost
            random_x = randint(0 , window_weight - 65)
            self.rect.y = 0
            self.rect.x = random_x
            lost += 1



enemy1 = Enemy(2, randint(0 , window_weight - 65), 0, "ufo.png")
enemy2 = Enemy(5, randint(0 , window_weight - 65), 0, "ufo.png")
enemy3 = Enemy(3, randint(0 , window_weight - 65), 0, "ufo.png")
enemy4 = Enemy(1, randint(0 , window_weight - 65), 0, "ufo.png")
enemy5 = Enemy(4, randint(0 , window_weight - 65), 0, "ufo.png")
enemy = sprite.Group()
enemy.add(enemy1)
enemy.add(enemy2)
enemy.add(enemy3)
enemy.add(enemy4)
enemy.add(enemy5)
asteroid1 = Enemy(1, randint(0 , window_weight - 65),0,'asteroid.png')
asteroid2 = Enemy(1, randint(0 , window_weight - 65),0,'asteroid.png')
asteroid3 = Enemy(1, randint(0 , window_weight - 65),0,'asteroid.png')
asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
player = Player(10,100, window_height-65,"rocket.png")
game = True
finish = False
while game:
    display.update()
    if not(finish):

        losting = font1.render('Пропущенно: ' + str(lost), True, (255, 255, 255))
        killing = font1.render("Поверженно: " + str(kills), True, (255, 255, 255))
        #lives = font1.render('Количество жизней:'+ str(amount_lives),True,(255, 255, 255) )
        window.blit(background, (0, 0))
        window.blit(losting,(10, 10))
        window.blit(killing, (10, 30))
        #window.blit(lives,(10, 50))
        player.reset()
        player.update()
        enemy.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        bullets.update()
        sprites_list1 = sprite.groupcollide(enemy, bullets, True, True)
        sprites_list2= sprite.groupcollide(asteroids, bullets, True, True)
        if sprite.spritecollide(player, asteroids, True):
            sprite.spritecollide(player, asteroids, True)
            amount_lives -= 1
            asteroid4 = Enemy(5, randint(0, window_weight - 65), 0, "asteroid.png")
            asteroids.add(asteroid4)

        lives = font1.render('Количество жизней:' + str(amount_lives), False, (255, 255, 255))
        window.blit(lives, (10, 50))
        if amount_lives == 0:
            finish = True
            loser = font2.render("Поражение", True, (255, 0, 0))
            window.blit(loser, (200, 200))
        if kills == 10:
            finish = True
            winner = font2.render("Победа", True, (255, 229, 0))
            window.blit(winner,(250, 200))

        if lost == 300:
            finish = True
            loser = font2.render("Поражение", True, (255, 0, 0))
            window.blit(loser,(200, 200) )
        enemy.update()
        asteroids.update()
        if sprite.spritecollide(player, enemy, False):
            finish = True
            loser = font2.render("Поражение", True, (255, 0, 0))
            window.blit(loser, (200, 200))




        for i in sprites_list1:
            enemy6 = Enemy(5, randint(0 , window_weight - 65), 0, "ufo.png")
            enemy.add(enemy6)
            kills += 1
        for i in sprites_list2:
            asteroid4 = Enemy(3, randint(0 , window_weight - 65), 0, "asteroid.png")
            asteroids.add(asteroid4)
        if rel_time:
            now_time = t()
            print(now_time - timer)
            if now_time - timer < 2:
                tim = font2.render("Перезарядка", True, (255, 255, 255))
                window.blit(tim, (200, 200))
            else:
                rel_time = False
                num_fire = 0
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                num_fire += 1

                if num_fire >= 12:
                    rel_time = True
                    timer = t()
                if rel_time == False:
                    player.fire()
                    firem = mixer.Sound("fire.ogg")
                    firem.play()

    clock.tick(FPS)
    display.update()
#dddddd