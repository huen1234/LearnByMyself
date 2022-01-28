
import pygame
import random
import os

FPS = 60
WHITE = (255,255,255)
WIDTH = 500
HEIGHT = 600

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH,HEIGHT)) 

pygame.display.set_caption("BOOMBOOM")

backgroundimg = pygame.image.load(os.path.join("img","background.png")).convert()
playerimg = pygame.image.load(os.path.join("img","player.png")).convert()
#rockimg = pygame.image.load(os.path.join("img","rock.png")).convert()
rockimgs = []
for i in range(7):
    rockimgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())
bulletimg = pygame.image.load(os.path.join("img","bullet.png")).convert()

fontname = pygame.font.match_font("arial")

def draw_text (surf, text, size, x,y):
    font = pygame.font.Font(fontname, size)
    textsurface = font.render(text,True, (255,255,255))
    textrect = textsurface.get_rect()
    textrect.centerx = x
    textrect.top = y
    surf.blit(textsurface, textrect)


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

    def update(self):
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
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bulletgrp.add(bullet)


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


all_sprites = pygame.sprite.Group()
rockgrp = pygame.sprite.Group()
bulletgrp = pygame.sprite.Group()


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
        r = Rock() 
        all_sprites.add(r)
        rockgrp.add(r)

    hits = pygame.sprite.spritecollide(player, rockgrp , False, pygame.sprite.collide_circle)
    if hits:
        running = False   

    #display
    screen.fill((0,0,0))
    screen.blit(backgroundimg,(0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(int(score)), 18, WIDTH/2, 10)
    pygame.display.update()

    #delay



pygame.QUIT()