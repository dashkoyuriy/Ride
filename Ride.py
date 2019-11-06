import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60
n_bullet = 0
n_hit = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()


def draw_text(surf, My_text, size, x, y):
    text = font.render(My_text, True, (0, 0, 0))
    screen.blit(text, [x, y])


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        global n_bullet
        bullet = Bullet(self.rect.centerx, self.rect.top)
        n_bullet += 1
        all_sprites.add(bullet)
        bullets.add(bullet)


class Goal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
goals = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Goal()
    all_sprites.add(m)
    goals.add(m)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()
    hits = pygame.sprite.groupcollide(goals, bullets, True, True)
    for hit in hits:
        m = Goal()
        all_sprites.add(m)
        goals.add(m)
        n_hit += 1

    hits = pygame.sprite.spritecollide(player, goals, False)
    if hits:
        running = False

    screen.fill((0, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()

screen = pygame.display.set_mode((250, 250))
pygame.display.set_caption("Result game")
screen.fill((0, 255, 255))
font = pygame.font.Font(None, 25)
draw_text(screen, "Number of bullets = " + str(n_bullet), 18, 20, 20)
draw_text(screen, "Number of hits = " + str(n_hit), 18, 20, 60)
try:
    draw_text(screen, "Shooting accuracy = " + str(int(100 * n_hit / n_bullet)) + "%", 18, 20, 100)
except ZeroDivisionError:
    draw_text(screen, "You didn't fire a shot!", 18, 20, 100)

pygame.display.flip()
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()