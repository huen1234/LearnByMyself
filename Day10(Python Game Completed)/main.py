
from ctypes import sizeof
from tkinter import CENTER
import pygame
import random
import os

FPS = 60
WHITE = (255,255,255)
WIDTH = 500
HEIGHT = 600

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH,HEIGHT)) 


pygame.display.set_caption("BOOMBOOM")

#load sound
shootsound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
explsound = [pygame.mixer.Sound(os.path.join("sound","expl0.wav")),pygame.mixer.Sound(os.path.join("sound","expl1.wav"))]


backgroundimg = pygame.image.load(os.path.join("img","background.png")).convert()
playerimg = pygame.image.load(os.path.join("img","player.png")).convert()
playerminiimg = pygame.transform.scale(playerimg,(25,19))
playerminiimg.set_colorkey((0,0,0))
#rockimg = pygame.image.load(os.path.join("img","rock.png")).convert()
rockimgs = []
for i in range(7):
    rockimgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

explanim = {}
explanim ['lg'] = []
explanim ['sml'] = []
explanim ['player'] = []
for i in range(9):
    explimg = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    explimg.set_colorkey((0,0,0))
    explanim['lg'].append(pygame.transform.scale(explimg,(75,75)))
    explanim['sml'].append(pygame.transform.scale(explimg,(30,30)))
    playerexpl = pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    playerexpl.set_colorkey((0,0,0))
    explanim['player'].append(playerexpl)
powerimgs = {}
powerimgs['shield'] = pygame.image.load(os.path.join("img","shield.png")).convert()
powerimgs['gun'] = pygame.image.load(os.path.join("img","gun.png")).convert()

bulletimg = pygame.image.load(os.path.join("img","bullet.png")).convert()

fontname = pygame.font.match_font("arial")

def draw_text (surf, text, size, x,y):
    font = pygame.font.Font(fontname, size)
    textsurface = font.render(text,True, (255,255,255))
    textrect = textsurface.get_rect()
    textrect.centerx = x
    textrect.top = y
    surf.blit(textsurface, textrect)

def draw_health(surf,hp,x,y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,(255,255,0),fill_rect)
    pygame.draw.rect(surf,(0,0,0),outline_rect, 2)

def draw_life (surf,lives, img,x,y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)


score = 0


#Sprite init
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerimg,(50,38))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom = (HEIGHT-10)
        self.speedx = 8
        self.radius = 20
        self.health = 100
        self.life = 3
        self.hidden = False
        self.hidetime = 0
        self.gun = 1
        self.guntime = 0


    def update(self):
        if self.gun > 1 and pygame.time.get_ticks() - self.guntime > 5000:
            self.gun -= 1 
            self.guntime = pygame.time.get_ticks()


        if (self.hidden == True) and pygame.time.get_ticks() - self.hidetime > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:  
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedx
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH 
    
    def shoot(self):
        if self.hidden == False:
            if self.gun == 1:  
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bulletgrp.add(bullet)
                shootsound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bulletgrp.add(bullet1)
                bulletgrp.add(bullet2)
                shootsound.play()

    def hide(self):
        self.hidden = True
        self.hidetime = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun +=1 
        self.gun_time = pygame.time.get_ticks()


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imageori = random.choice(rockimgs)
        self.imageori.set_colorkey((0,0,0))
        self.image = self.imageori.copy()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        self.radius = self.rect.width*0.85/2
        self.total_degree = 0
        self.rot_degree = 3

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.imageori,self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #if the rock out of the boarder
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0 :
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletimg  
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explanim[self.size][0] 
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explanim[self.size]):
                self.kill()
            else:
                self.image = explanim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerimgs[self.type]
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


all_sprites = pygame.sprite.Group()
rockgrp = pygame.sprite.Group()
bulletgrp = pygame.sprite.Group()
powers = pygame.sprite.Group()


player = Player()
all_sprites.add(player)
for i in range(8):
    rock = Rock()
    all_sprites.add(rock)
    rockgrp.add(rock)



running = True
while running:
    clock.tick(FPS)
    #input
    for event in pygame.event.get(): #a list of event happen in the window 
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #refresh
    all_sprites.update()

    #determination
    hits = pygame.sprite.groupcollide(rockgrp,bulletgrp, True, True)
    for hit in hits:
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        random.choice(explsound).play() 
        r = Rock() 
        all_sprites.add(r)
        rockgrp.add(r)
        if random.random() > 0.1:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)

    hits = pygame.sprite.spritecollide(player, rockgrp , True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius
        r = Rock() 
        all_sprites.add(r)
        rockgrp.add(r)
        if player.health <= 0:
            die = Explosion(player.rect.center, 'player')
            all_sprites.add(die)
            player.life -= 1
            player.health = 100
            player.hide()
        if player.life == 0 and not(die.alive()):
            running = False
    

    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
        elif hit.type == 'gun':
            player.gunup()


    #display
    screen.fill((0,0,0))
    screen.blit(backgroundimg,(0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(int(score)), 18, WIDTH/2, 10)
    draw_health(screen,player.health,5,10)
    draw_life(screen, player.life, playerminiimg, WIDTH-100, 15)
    pygame.display.update()

    #delay



pygame.QUIT()