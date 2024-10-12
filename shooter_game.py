from pygame import *
from random import *
font.init()

score = 0
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
lost = 0
FPS=10
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial',70)
lose_text = font2.render('YOU LOSE!!!',True,(255,0,0))
win_text = font2.render('YOU WIN!!!',True,(255,215,0))
win_width = 700
win_height = 800
window=display.set_mode((win_width,win_height))
display.set_caption("Space invaders")
background=transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
flag = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 625:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top,5,15,-8)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= win_height + 25:
            self.rect.y = 0
            self.rect.x = randint(5, 625)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y == 0:
            self.kill()

monsters = sprite.Group()
bullets = sprite.Group()

ship = Player('rocket.png',310,win_height-100,70,90,9)
for i in range(1,6):
    enemy = Enemy('ufo.png',randint(5,625),0,50,50,i)
    monsters.add(enemy)

while flag:
    for ivent in event.get():
        if ivent.type == QUIT:
            flag = False
        elif ivent.type == KEYDOWN:
            if ivent.key == K_SPACE:
                ship.fire()
                fire_sound.play()

    if not finish:
        window.blit(background,(0,0))
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for i in collides:
            score += 1
            enemy = Enemy('ufo.png',randint(5,625),0,50,50,randint(1,6))
            monsters.add(enemy)           
        if lost >= 3 or sprite.spritecollide(ship,monsters,False):
            window.blit(lose_text,(win_width / 2,win_height / 2))
            finish = True
            mixer.music.stop()
        if score >= 10:
            window.blit(win_text,(win_width / 2,win_height / 2))
            finish = True
            mixer.music.stop()
        win = font1.render('Счёт: ' + str(score),True,(255,255,255))
        lose = font1.render('Пропущено: ' + str(lost),True,(255,255,255))
        window.blit(win,(10,10))
        window.blit(lose,(10,50))
        ship.update()
        ship.reset()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        display.update()
    time.delay(FPS)

    