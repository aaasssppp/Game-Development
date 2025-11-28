import pygame
import random

pygame.init()

# window
w_width = 660
w_height = 600
window = pygame.display.set_mode((w_width,w_height))
pygame.display.set_caption("Spaceship")

# loading images
bg = pygame.image.load("Spaceship/media/bg.png")
bg = pygame.transform.scale(bg,(w_width,w_height))
spaceship_img = pygame.image.load("Spaceship/media/spaceship.png")
bullet = pygame.image.load("Spaceship/media/bullet.png")
enemy_img = [pygame.image.load(f"Spaceship/media/alien{i}.png") for i in range(1,6)]
enemy_bullet = pygame.image.load(f"Spaceship/media/alien_bullet.png")
enemy = []

# game variables
clock = pygame.time.Clock()
bullets = []
shoot_counter = 0
rows = 4
cols = 5
alien_cooldown = 1000 # 1 sec for alien to cooldown before shooting
last_alien_shot = pygame.time.get_ticks() # set the start game time to the last time the alien shot - so that after 1 sec the game start only the alien will shoot
alien_bullets = []

# spaceship class
class Spaceship():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 75
        self.height = 75
        self.vel = 8
        self.rect = (self.x,self.y,self.width,self.height)
        self.health = 5
        self.alive = True

    def draw(self,window):
        window.blit(spaceship_img, (self.x,self.y))
        pygame.draw.rect(window, "red", (self.x, self.y+self.height, self.width, 10)) # health bar
        pygame.draw.rect(window, "green", (self.x, self.y+self.height, round(self.width* (self.health/5)), 10))
        self.rect = (self.x, self.y, self.width, self.height) # hit box's updated rectangle values

# class projectile
class Projectile():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 3

    def draw(self,window):
        self.y -= self.vel
        window.blit(bullet, (self.x, self.y))

# class enemies
class Enemies():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = enemy_img[random.randint(0,4)] # random alien image
        self.move_counter = 0
        self.direction = 1

    def draw(self,window):
        window.blit(self.image, (self.x,self.y))
        self.x += self.direction
        self.move_counter += 1
        if abs(self.move_counter) > 100:
            self.direction *= -1
            self.move_counter *= self.direction

# class enemy projectiles
class Enemy_projectiles():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel = 2

    def draw(self,window):
        self.y += self.vel
        window.blit(enemy_bullet, (self.x, self.y))

# game objects
# spaceship
spaceship = Spaceship(round(w_width/2)-34, w_height-100) # spaceship width = 75, to make it centerd 75/2 = 34 -> subract fromt the x cord to make it the ship perfectly centred
# aliens
for row in range(rows):
    for col in range(cols):
        enemy.append((Enemies(100+col*100, 100+row*70))) # we are mult the value, so that each alien has equal spacing (vertical and horizontal spacing) - we are mult the value, so the aliens will be oscilation back and forth by 100 

# drawing on the window surface
def DrawInGameLoop():
    global window
    clock.tick(60) # 60 fps
    window.blit(bg, (0,0)) # set the bg at the 0,0 where the window is starting
    spaceship.draw(window) # drawing spaceship
    for projectile in bullets: # drawing projectiles from spaceship
        projectile.draw(window)
    for enem in enemy: # drawing alien enemies
        enem.draw(window)
    for alien_bullet in alien_bullets: # drawing projectiles from alien enemies
        alien_bullet.draw(window)
    pygame.display.flip()
        

# game loop
run = True
while run:
    # user press exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # adding enemy projectiles
    time_now = pygame.time.get_ticks() # current game time
    if time_now - last_alien_shot > alien_cooldown and len(alien_bullets) < 5 and len(enemy) > 0:
        attacking_alien = random.choice(enemy) # randomly choosing an alien to shoot
        alien_bullet = Enemy_projectiles(attacking_alien.x+25, attacking_alien.y+50) # 25 is half of the width and 50 is height of the alien - so that the bullet starts below alien and from center aligned to horizontal axis - so that the bullet will start from the mid of alien
        alien_bullets.append(alien_bullet)
        last_alien_shot = time_now # set last alien shot time to now

    # removing bullets from list
    for alien_bullet in alien_bullets:
        if alien_bullet.y > w_height:
            alien_bullets.remove(alien_bullet)

    # to avoid continous firing of bullets
    if shoot_counter > 0:
        shoot_counter += 1
    if shoot_counter > 10:
        shoot_counter = 0
    for projectile in bullets:
        if projectile.y > 0:
            projectile.y -= projectile.vel
        else:
            bullets.pop(bullets.index(projectile))

    # user input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and spaceship.x > 0:
        spaceship.x -= spaceship.vel
    elif keys[pygame.K_RIGHT] and spaceship.x < w_width - spaceship.width:
        spaceship.x += spaceship.vel
    if keys[pygame.K_SPACE] and shoot_counter == 0:
        if len(bullets) < 5:
            bullets.append(Projectile(spaceship.x + round(spaceship.width/2), spaceship.y))

        shoot_counter = 1
    DrawInGameLoop()

pygame.quit()